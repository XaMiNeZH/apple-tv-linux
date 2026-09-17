from __future__ import annotations

from tvweb.main import parse_args


def test_parse_preferences_flag() -> None:
    args = parse_args(["--preferences"])
    assert args.preferences is True
    args = parse_args(["-p"])
    assert args.preferences is True
    args = parse_args([])
    assert args.preferences is False
