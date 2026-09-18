from __future__ import annotations

from tvweb.main import parse_args


def test_parse_preferences_flag() -> None:
    args = parse_args(["--preferences"])
    assert args.preferences is True
    assert args.fallback is False
    args = parse_args(["-p"])
    assert args.preferences is True
    args = parse_args([])
    assert args.preferences is False
    assert args.fallback is False


def test_parse_fallback_flag() -> None:
    args = parse_args(["--fallback"])
    assert args.fallback is True
    assert args.preferences is False
