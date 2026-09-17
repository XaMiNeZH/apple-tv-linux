# Install TV Web on Fedora Workstation

TV Web is a GNOME launcher around [tv.apple.com](https://tv.apple.com). Install a
browser that can actually play that site, then install the launcher.

## 1. Browser (Widevine)

Firefox is enough for playback. Chrome or Edge give a cleaner app window.

### Firefox (default on Fedora)

```bash
sudo dnf install firefox
```

Open Firefox once, visit a site that uses protected video if prompted, and allow
the Widevine plugin.

### Google Chrome (recommended window)

```bash
sudo dnf install fedora-workstation-repositories
sudo dnf config-manager setopt google-chrome.enabled=1
sudo dnf install google-chrome-stable
```

On older Fedora, the enable step is:

```bash
sudo dnf config-manager --set-enabled google-chrome
```

### Microsoft Edge (optional)

Install Edge from Microsoft’s Fedora repo if you already use it. TV Web will
detect `microsoft-edge-stable`.

Do not rely on Fedora **Chromium** for Apple TV on the web. It is often built
without Widevine.

## 2. Build dependencies

```bash
sudo dnf install python3-gobject gtk4 libadwaita meson ninja-build
```

## 3. Install for your user

From the repository root:

```bash
meson setup build --prefix="$HOME/.local"
meson install -C build
gtk-update-icon-cache "$HOME/.local/share/icons/hicolor" >/dev/null 2>&1 || true
update-desktop-database "$HOME/.local/share/applications" >/dev/null 2>&1 || true
```

`$HOME/.local/bin` must be on your `PATH` (Fedora Workstation usually does this
after a session restart).

## 4. First run

Open **TV Web** from the app grid, or:

```bash
tvweb --preferences
```

Pick Chrome/Edge if installed, leave hardware decoding on unless video is blank,
then click **Open**. Later launches go straight to the site.

## Data

| Path | Purpose |
| --- | --- |
| `~/.config/tvweb/config.json` | Browser choice and flags |
| `~/.local/share/tvweb/profiles/` | Dedicated browser profile (keeps you signed in) |

## Wayland and VAAPI

Chrome/Edge are started with `--ozone-platform-hint=auto`. Hardware decoding
adds VAAPI feature flags. If the picture is a black frame, open preferences and
turn hardware decoding off.

## Quality

This is the website, not Apple’s Windows/macOS apps. Resolution and audio follow
whatever Apple sends to Linux browsers for your Apple account region.
