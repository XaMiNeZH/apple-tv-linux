"""TV Web entry point."""

from __future__ import annotations

import argparse
import sys

from tvweb.browsers import detect_browsers, pick_browser
from tvweb.config import load_config, profile_dir, save_config, Config
from tvweb.launcher import launch


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="tvweb",
        description="Unofficial GNOME wrapper for tv.apple.com",
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


def main(argv: list[str] | None = None) -> int:
    parse_args(argv)
    config = load_config()
    browsers = detect_browsers()
    browser = pick_browser(browsers, config.browser_id)
    if browser is None:
        _print_missing_browser()
        return 1
    if not config.completed_first_run:
        save_config(
            Config(
                browser_id=browser.id,
                hardware_decode=config.hardware_decode,
                completed_first_run=True,
            )
        )
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


if __name__ == "__main__":
    raise SystemExit(main())
