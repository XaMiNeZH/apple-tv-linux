# TV Web

Unofficial Fedora GNOME **desktop app** for [tv.apple.com](https://tv.apple.com).

It is **not** an Apple product and is **not** affiliated with Apple. TV Web is its
own window, icon, and process. Apple TV still runs inside that window (the
official website), so picture and sound match the Linux web player — not the
Windows or macOS apps.

## What you get

- A **TV Web** app in GNOME (not a browser tab, not “open Chrome”)
- Splash screen, then Apple TV fills the window
- Sign-in stays in the app (`persist:tvweb` profile)
- Apple account popups open as extra TV Web windows
- Fullscreen, reload, and a single-instance lock
- Optional VAAPI / Wayland flags

## What you do not get

- 4K, Dolby Vision, or Dolby Atmos
- The Windows/macOS Apple TV client
- Region rules different from tv.apple.com (Moroccan Apple accounts follow the website)

## Install on Fedora

Download a Linux build from [Releases](https://github.com/XaMiNeZH/apple-tv-linux/releases):

```bash
chmod +x tvweb-0.2.0-x86_64.AppImage
./tvweb-0.2.0-x86_64.AppImage
```

Or build from source (needs **Node.js 20+**). Chrome or Edge on the machine still helps protected playback (Widevine).

```bash
sudo dnf install nodejs git gtk4 libadwaita python3-gobject
git clone https://github.com/XaMiNeZH/apple-tv-linux.git
cd apple-tv-linux
chmod +x scripts/install-fedora.sh
./scripts/install-fedora.sh
```

Open **TV Web** from the GNOME app grid.

From a checkout without installing:

```bash
npm install
npm start
```

`--preferences` still opens the older GNOME browser-fallback settings.

## Tests

```bash
python3 -m pytest
```

## License

MIT. Apple, Apple TV, and related marks belong to Apple Inc.
