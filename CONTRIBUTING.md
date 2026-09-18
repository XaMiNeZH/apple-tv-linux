# Contributing

TV Web stays small: the official `tv.apple.com` website in a Linux desktop
shell, with a browser fallback.

## Before a change

- Keep Electron as the default app.
- Keep the GTK4/libadwaita fallback working.
- Do not add DRM circumvention or unofficial streaming APIs.
- Do not claim playback quality the Linux website cannot promise.
- Use original or properly licensed assets.

## Check your work

```bash
npm install
npm run test:electron
npm run pack
python3 -m pytest
```

For Electron changes, test the first run, a second launch, an external link,
fullscreen, and the offline retry screen.

For packaging changes, confirm the GNOME icon and window association. Keep user
data when uninstalling unless the user explicitly asks to remove it.
