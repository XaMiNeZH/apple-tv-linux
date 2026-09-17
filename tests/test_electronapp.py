from __future__ import annotations

from pathlib import Path

from tvweb.electronapp import electron_app_dir, electron_cli


def test_electron_cli_reads_env(tmp_path: Path, monkeypatch) -> None:
    binary = tmp_path / "tvweb"
    binary.write_text("", encoding="utf-8")
    binary.chmod(0o755)
    monkeypatch.setenv("TVWEB_ELECTRON", str(binary))
    assert electron_cli() == binary


def test_electron_app_dir_env(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("TVWEB_APP_DIR", str(tmp_path))
    assert electron_app_dir() == tmp_path
