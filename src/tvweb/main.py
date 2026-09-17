"""TV Web entry point."""

from __future__ import annotations

import argparse
import sys


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


def main(argv: list[str] | None = None) -> int:
    parse_args(argv)
    print("TV Web: browser launcher is not wired up yet.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
