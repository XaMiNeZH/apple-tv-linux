# Install TV Web on Fedora Workstation

TV Web is a GNOME desktop app. It hosts [tv.apple.com](https://tv.apple.com) in
its own window (Electron/Chromium), not by launching your browser.

## 1. Tools

```bash
sudo dnf install git nodejs gtk4 libadwaita python3-gobject
```

Install **Google Chrome** or **Microsoft Edge** as well. Apple’s website uses
Widevine; those browsers ship the CDM that Linux Chromium apps rely on.

```bash
sudo dnf install fedora-workstation-repositories
sudo dnf config-manager setopt google-chrome.enabled=1
sudo dnf install google-chrome-stable
```

## 2. Install the app

### From Releases (recommended)

Download the latest **AppImage** or **.tar.gz** from
[Releases](https://github.com/XaMiNeZH/apple-tv-linux/releases).

```bash
chmod +x tvweb-*-x86_64.AppImage
./tvweb-*-x86_64.AppImage
```

### From source

```bash
git clone https://github.com/XaMiNeZH/apple-tv-linux.git
cd apple-tv-linux
chmod +x scripts/install-fedora.sh
./scripts/install-fedora.sh
```

That builds TV Web and puts it in `~/.local/lib/tvweb`, with a launcher in
`~/.local/bin` and a GNOME desktop entry.

`$HOME/.local/bin` must be on your `PATH`. Then open **TV Web** from the app
grid.

## 3. Run from git

```bash
npm install
npm start
```

## Data

| Path | Purpose |
| --- | --- |
| `~/.config/TV Web/` | Electron profile (keeps you signed in) |
| `~/.config/tvweb/config.json` | Fallback browser launcher settings |

## Quality

This is still Apple’s website inside a desktop shell. Resolution and audio
follow whatever Apple sends to Linux browsers for your account region.
