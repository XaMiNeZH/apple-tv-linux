# Architecture

TV Web has one product and two launch paths.

## Electron app (default)

```text
tv.apple.com
  └─ isolated preload (small, allow-listed IPC)
       └─ Electron main process
            ├─ trusted Apple-domain navigation
            ├─ external links → default browser
            ├─ first-run and offline pages
            └─ local window state + persistent web profile
```

- `app/main.mjs` owns windows, menus, links, and lifecycle.
- `app/preload.mjs` exposes only first-run, navigation, and help actions.
- `app/navigation.mjs` keeps hostname checks testable and exact.
- `app/state.mjs` stores first-run completion and window size.
- `persist:tvweb` stores Apple’s cookies and website data separately.

The app loads the official website. It does not call an unofficial catalog or
streaming API, alter media, or bypass DRM.

## GTK browser fallback

```text
GTK4/libadwaita setup
  └─ selected installed browser
       └─ dedicated TV Web profile → tv.apple.com
```

`src/tvweb/` detects Chrome, Edge, and Firefox, saves a small XDG config, and
starts the selected browser in app mode. Use `--fallback` to select this path
explicitly.

## Linux packaging

`electron-builder` produces AppImage, RPM, and tar.gz files for x86-64 and
ARM64. The release workflow:

1. skips versions already published,
2. runs Electron and Python tests,
3. builds both architectures,
4. uploads all six files to a draft,
5. publishes only after every upload succeeds.

The separate test workflow also checks dependencies and smoke-tests packaging
on every main-branch change and pull request.
