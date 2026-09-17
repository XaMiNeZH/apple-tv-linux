"""XDG config for TV Web."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path

from tvweb import CONFIG_APP_DIR, DATA_APP_DIR


@dataclass
class Config:
    browser_id: str | None = None
    hardware_decode: bool = True
    completed_first_run: bool = False


def xdg_config_home() -> Path:
    raw = os.environ.get("XDG_CONFIG_HOME")
    if raw:
        return Path(raw)
    return Path.home() / ".config"


def xdg_data_home() -> Path:
    raw = os.environ.get("XDG_DATA_HOME")
    if raw:
        return Path(raw)
    return Path.home() / ".local" / "share"


def config_path() -> Path:
    return xdg_config_home() / CONFIG_APP_DIR / "config.json"


def data_dir() -> Path:
    return xdg_data_home() / DATA_APP_DIR


def profile_dir(browser_id: str) -> Path:
    return data_dir() / "profiles" / browser_id


def load_config() -> Config:
    path = config_path()
    if not path.is_file():
        return Config()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return Config()
    if not isinstance(payload, dict):
        return Config()
    return Config(
        browser_id=payload.get("browser_id") or None,
        hardware_decode=bool(payload.get("hardware_decode", True)),
        completed_first_run=bool(payload.get("completed_first_run", False)),
    )


def save_config(config: Config) -> None:
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(asdict(config), indent=2) + "\n",
        encoding="utf-8",
    )
