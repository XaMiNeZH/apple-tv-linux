"""TV Web entry point."""

from __future__ import annotations

import argparse
import os
import sys

from tvweb.browsers import detect_browsers, pick_browser
from tvweb.config import load_config, profile_dir
from tvweb.electronapp import electron_app_dir, electron_cli
from tvweb.launcher import launch


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="tvweb",
        description="Unofficial GNOME desktop app for tv.apple.com",
    )
    parser.add_argument(
        "--preferences",
        "-p",
        action="store_true",
        help="Open first-run / preferences instead of launching",
    )
    return parser.parse_args(argv)


def _print_missing_browser() -> None:
    print(
        "TV Web could not find Google Chrome, Microsoft Edge, or Firefox.\n"
        "Install one of those so tv.apple.com can play protected video.\n"
        "On Fedora Workstation:\n"
        "  sudo dnf install firefox\n"
        "  # or Google Chrome from Google's Fedora repo\n",
        file=sys.stderr,
    )


def _print_missing_gtk() -> None:
    print(
        "Preferences need GTK 4 and libadwaita.\n"
        "On Fedora Workstation:\n"
        "  sudo dnf install python3-gobject gtk4 libadwaita\n",
        file=sys.stderr,
    )


def _launch_electron() -> int | None:
    electron = electron_cli()
    if electron is None:
        return None
    app_dir = electron_app_dir()
    argv = [str(electron)]
    if electron.name == "electron":
        if not (app_dir / "app" / "main.mjs").is_file():
            return None
        argv.append(str(app_dir))
    os.execv(str(electron), argv)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.preferences:
        launched = _launch_electron()
        if launched is not None:
            return launched
    config = load_config()
    browsers = detect_browsers()

    show_prefs = args.preferences or not config.completed_first_run
    if not show_prefs:
        browser = pick_browser(browsers, config.browser_id)
        if browser is None:
            _print_missing_browser()
            show_prefs = True
        else:
            try:
                launch(
                    browser,
                    profile=profile_dir(browser.id),
                    hardware_decode=config.hardware_decode,
                    replace_process=True,
                )
            except OSError as exc:
                print(f"TV Web could not start {browser.path}: {exc}", file=sys.stderr)
                return 1
            return 0

    if not browsers:
        _print_missing_browser()

    try:
        from tvweb.window import run_preferences
    except (ImportError, ValueError):
        _print_missing_gtk()
        return 1

    remaining = [sys.argv[0]]
    return run_preferences(config, remaining)


if __name__ == "__main__":
    raise SystemExit(main())
