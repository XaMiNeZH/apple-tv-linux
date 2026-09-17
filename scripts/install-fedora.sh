#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"

need() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Install $1 first." >&2
    exit 1
  }
}

need npm
need node

npm install
npm run pack

lib="$HOME/.local/lib/tvweb"
bin="$HOME/.local/bin"
apps="$HOME/.local/share/applications"
icons="$HOME/.local/share/icons/hicolor/scalable/apps"
unpacked="$root/dist/linux-unpacked"

if [[ ! -x "$unpacked/tvweb" ]]; then
  echo "electron-builder did not produce $unpacked/tvweb" >&2
  exit 1
fi

mkdir -p "$lib" "$bin" "$apps" "$icons"
rm -rf "$lib"
cp -a "$unpacked" "$lib"
ln -sfn "$lib/tvweb" "$bin/tvweb"
install -m 644 "$root/data/xyz.xaminezh.TvWeb.desktop" "$apps/xyz.xaminezh.TvWeb.desktop"
install -m 644 "$root/data/icons/hicolor/scalable/apps/xyz.xaminezh.TvWeb.svg" \
  "$icons/xyz.xaminezh.TvWeb.svg"

gtk-update-icon-cache "$HOME/.local/share/icons/hicolor" >/dev/null 2>&1 || true
update-desktop-database "$apps" >/dev/null 2>&1 || true

echo "Installed TV Web. Make sure $bin is on your PATH, then open TV Web from GNOME."
