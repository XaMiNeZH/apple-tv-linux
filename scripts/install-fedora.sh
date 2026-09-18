#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"

lib="$HOME/.local/lib/tvweb"
bin="${XDG_BIN_HOME:-$HOME/.local/bin}"
data_home="${XDG_DATA_HOME:-$HOME/.local/share}"
apps="$data_home/applications"
icons="$data_home/icons/hicolor/scalable/apps"
metainfo="$data_home/metainfo"

need() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Install $1 first." >&2
    exit 1
  }
}

refresh_desktop() {
  if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -f "$data_home/icons/hicolor" >/dev/null 2>&1 || true
  fi
  if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$apps" >/dev/null 2>&1 || true
  fi
}

case "${1:-}" in
  --uninstall)
    rm -rf "$lib"
    rm -f \
      "$bin/tvweb" \
      "$apps/xyz.xaminezh.TvWeb.desktop" \
      "$icons/xyz.xaminezh.TvWeb.svg" \
      "$metainfo/xyz.xaminezh.TvWeb.metainfo.xml"
    refresh_desktop
    echo "TV Web was removed. Your sign-in data was left in ~/.config/TV Web."
    exit 0
    ;;
  "")
    ;;
  *)
    echo "Usage: $0 [--uninstall]" >&2
    exit 2
    ;;
esac

need npm
need node

npm install
npm run pack

unpacked="$root/dist/linux-unpacked"

if [[ ! -x "$unpacked/tvweb" ]]; then
  echo "electron-builder did not produce $unpacked/tvweb" >&2
  exit 1
fi

mkdir -p "$bin" "$apps" "$icons" "$metainfo"
rm -rf "$lib"
cp -a "$unpacked" "$lib"
ln -sfn "$lib/tvweb" "$bin/tvweb"
install -m 644 "$root/data/xyz.xaminezh.TvWeb.desktop" "$apps/xyz.xaminezh.TvWeb.desktop"
install -m 644 "$root/data/icons/hicolor/scalable/apps/xyz.xaminezh.TvWeb.svg" \
  "$icons/xyz.xaminezh.TvWeb.svg"
install -m 644 "$root/data/xyz.xaminezh.TvWeb.metainfo.xml" \
  "$metainfo/xyz.xaminezh.TvWeb.metainfo.xml"

refresh_desktop

echo "TV Web is installed. Open it from the GNOME app grid."
if [[ ":$PATH:" != *":$bin:"* ]]; then
  echo "Tip: add $bin to PATH to run 'tvweb' from a terminal."
fi
