from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path

from tvweb import __version__


def test_project_versions_match() -> None:
    root = Path(__file__).parents[1]
    package = json.loads((root / "package.json").read_text(encoding="utf-8"))
    with (root / "pyproject.toml").open("rb") as stream:
        python_project = tomllib.load(stream)
    meson = (root / "meson.build").read_text(encoding="utf-8")
    meson_version = re.search(r"version: '([^']+)'", meson)

    assert meson_version is not None
    versions = {
        package["version"],
        python_project["project"]["version"],
        meson_version.group(1),
        __version__,
    }
    assert len(versions) == 1
