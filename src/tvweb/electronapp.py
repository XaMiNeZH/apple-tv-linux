"""Resolve the bundled TV Web desktop app (Electron), if present."""

from __future__ import annotations

import os
from pathlib import Path


def repo_root() -> Path:
    here = Path(__file__).resolve()
    source_root = here.parents[2]
    if (source_root / "app" / "main.mjs").is_file():
        return source_root
    installed = here.parents[1]
    if (installed / "app" / "main.mjs").is_file():
        return installed
    return source_root


def electron_cli() -> Path | None:
    env = os.environ.get("TVWEB_ELECTRON")
    if env:
        path = Path(env)
        if path.is_file():
            return path

    root = repo_root()
    candidates = [
        Path.home() / ".local" / "lib" / "tvweb" / "tvweb",
        root / "dist" / "linux-unpacked" / "tvweb",
        root / "node_modules" / ".bin" / "electron",
    ]
    for path in candidates:
        if path.is_file():
            return path
    return None


def electron_app_dir() -> Path:
    env = os.environ.get("TVWEB_APP_DIR")
    if env:
        return Path(env)
    return repo_root()
