# TV Web

Unofficial Fedora GNOME desktop wrapper for [tv.apple.com](https://tv.apple.com).

It is **not** an Apple product and is **not** affiliated with Apple. There is no
Linux Apple TV app. This project opens the official website in its own window and
browser profile so it shows up in the GNOME app grid instead of a browser tab.

## What you get

- A **TV Web** icon in GNOME
- Chrome or Edge **app mode** (no tab strip or address bar)
- Firefox fallback with a dedicated profile
- Stay signed in (`~/.local/share/tvweb/`)
- Optional VAAPI hardware-decode flags
- First-run / preferences (`tvweb --preferences`)

## What you do not get

Playback is the **Linux web player**, the same as Chrome or Firefox:

- Not 4K, Dolby Vision, or Dolby Atmos
- Not the Windows or macOS Apple TV apps
- Same Apple account and **region rules as the website** (including a Moroccan
  Apple account on the web)

## Requirements

- Fedora Workstation (GNOME)
- Python 3.11+
- GTK 4, libadwaita, PyGObject
- A browser that can play tv.apple.com:
  - **Google Chrome** or **Microsoft Edge** (best app window)
  - **Firefox** (already on Fedora; weaker “app” chrome)
  - Distro **Chromium** is detected last and often **cannot** play protected video

## Install on Fedora

See [docs/fedora.md](docs/fedora.md).

```bash
sudo dnf install python3-gobject gtk4 libadwaita meson ninja-build firefox
meson setup build --prefix="$HOME/.local"
meson install -C build
gtk-update-icon-cache "$HOME/.local/share/icons/hicolor" >/dev/null 2>&1 || true
update-desktop-database "$HOME/.local/share/applications" >/dev/null 2>&1 || true
```

Search **TV Web** in GNOME and open it. The first launch asks which browser to use.

```bash
tvweb                 # open the site (after first run)
tvweb --preferences   # pick browser / hardware decode
```

Run from a git checkout without installing:

```bash
PYTHONPATH=src python3 -m tvweb --preferences
```

## Tests

```bash
python3 -m pytest
```

## License

MIT. Apple, Apple TV, and related marks belong to Apple Inc.
