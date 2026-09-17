from __future__ import annotations

from pathlib import Path

from tvweb.config import Config, load_config, profile_dir, save_config


def test_round_trip_config(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "data"))

    original = Config(
        browser_id="firefox",
        hardware_decode=False,
        completed_first_run=True,
    )
    save_config(original)
    loaded = load_config()
    assert loaded == original
    assert profile_dir("firefox") == tmp_path / "data" / "tvweb" / "profiles" / "firefox"


def test_missing_config_defaults(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    loaded = load_config()
    assert loaded.browser_id is None
    assert loaded.hardware_decode is True
    assert loaded.completed_first_run is False
