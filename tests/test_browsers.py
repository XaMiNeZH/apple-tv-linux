from __future__ import annotations

from pathlib import Path

from tvweb.browsers import detect_browsers, pick_browser


def _fake_binary(directory: Path, name: str) -> Path:
    path = directory / name
    path.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    path.chmod(0o755)
    return path


def test_prefers_chrome_over_chromium_and_firefox(tmp_path: Path, monkeypatch) -> None:
    bindir = tmp_path / "bin"
    bindir.mkdir()
    _fake_binary(bindir, "chromium")
    _fake_binary(bindir, "firefox")
    _fake_binary(bindir, "google-chrome-stable")
    monkeypatch.setenv("PATH", str(bindir))

    found = detect_browsers()
    assert [browser.id for browser in found] == [
        "google-chrome-stable",
        "firefox",
        "chromium",
    ]
    assert found[0].drm_likely is True
    assert found[0].kind == "chromium"
    assert found[2].drm_likely is False


def test_skips_missing_binaries(tmp_path: Path, monkeypatch) -> None:
    bindir = tmp_path / "bin"
    bindir.mkdir()
    _fake_binary(bindir, "firefox")
    monkeypatch.setenv("PATH", str(bindir))

    found = detect_browsers()
    assert len(found) == 1
    assert found[0].id == "firefox"
    assert found[0].kind == "firefox"


def test_pick_browser_uses_preferred_id(tmp_path: Path, monkeypatch) -> None:
    bindir = tmp_path / "bin"
    bindir.mkdir()
    _fake_binary(bindir, "google-chrome-stable")
    _fake_binary(bindir, "firefox")
    monkeypatch.setenv("PATH", str(bindir))

    found = detect_browsers()
    chosen = pick_browser(found, "firefox")
    assert chosen is not None
    assert chosen.id == "firefox"


def test_pick_browser_falls_back_to_first(tmp_path: Path, monkeypatch) -> None:
    bindir = tmp_path / "bin"
    bindir.mkdir()
    _fake_binary(bindir, "microsoft-edge-stable")
    monkeypatch.setenv("PATH", str(bindir))

    found = detect_browsers()
    chosen = pick_browser(found, "missing")
    assert chosen is not None
    assert chosen.id == "microsoft-edge-stable"
