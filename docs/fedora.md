# Install TV Web on Fedora Workstation

TV Web hosts [tv.apple.com](https://tv.apple.com) in a dedicated Electron
window. Fedora GNOME is the primary target.

## Recommended: RPM

Download the latest RPM from
[Releases](https://github.com/XaMiNeZH/apple-tv-linux/releases).

| CPU | Package label |
| --- | --- |
| Intel / AMD 64-bit | `x86_64` |
| ARM 64-bit | `arm64` or `aarch64` |

```bash
sudo dnf install ./tvweb-*-x86_64.rpm
```

Open **TV Web** from the GNOME app grid.

## Portable builds

AppImage runs without installing:

```bash
chmod +x tvweb-*-x86_64.AppImage
./tvweb-*-x86_64.AppImage
```

The tar.gz contains the same unpacked Electron app for scripts and portable
directories.

## Install from source

Requires Node.js 20+:

```bash
sudo dnf install git nodejs
git clone https://github.com/XaMiNeZH/apple-tv-linux.git
cd apple-tv-linux
./scripts/install-fedora.sh
```

This installs only for your user:

| Path | Purpose |
| --- | --- |
| `~/.local/lib/tvweb/` | Electron application |
| `~/.local/bin/tvweb` | Terminal launcher |
| `~/.local/share/applications/` | GNOME launcher |

To remove a source install:

```bash
./scripts/install-fedora.sh --uninstall
```

## Browser fallback

The source tree keeps a GTK4/libadwaita fallback. It opens a dedicated Chrome,
Edge, or Firefox profile instead of Electron.

Use it if the Electron runtime cannot play a protected title:

```bash
sudo dnf install python3-gobject gtk4 libadwaita firefox
PYTHONPATH=src python3 -m tvweb --fallback
```

Open its settings directly:

```bash
PYTHONPATH=src python3 -m tvweb --preferences
```

Chrome and Edge generally have the best chance of protected web playback.
Installing either browser does **not** add its DRM component to Electron; the
fallback launches that browser itself.

## Hardware decoding

Wayland/X11 selection is automatic. Experimental VAAPI flags are opt-in:

```bash
TVWEB_ENABLE_VAAPI=1 tvweb
```

Leave this off if video is blank, unstable, or already smooth. It does not
change the quality Apple serves.

## Troubleshooting

**A protected title does not play**

1. Check the same title on `https://tv.apple.com` in Chrome or Edge.
2. If it works there, use the [browser fallback](#browser-fallback).
3. If it fails there too, TV Web cannot override Apple’s Linux or region rules.

**The AppImage does not appear in the app grid**

AppImage is portable. Install the RPM for full GNOME integration.

**Reset the first-run screen**

Remove only the small state file (this does not sign you out):

```bash
rm -f ~/.config/TV\ Web/state.json
```

## Data and privacy

| Path | Purpose |
| --- | --- |
| `~/.config/TV Web/` | Electron profile, window state, and sign-in session |
| `~/.config/tvweb/config.json` | Fallback browser launcher settings |
| `~/.local/share/tvweb/profiles/` | Fallback browser profiles |

TV Web sends no custom analytics. Apple’s website follows Apple’s own terms and
privacy policy.
