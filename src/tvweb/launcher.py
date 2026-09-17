"""Build and run a dedicated tv.apple.com browser window."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from tvweb import APPLE_TV_URL, WINDOW_CLASS
from tvweb.browsers import Browser


def ensure_profile_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def build_command(
    browser: Browser,
    *,
    profile: Path,
    hardware_decode: bool = False,
) -> list[str]:
    if browser.kind == "firefox":
        ensure_profile_dir(profile)
        return [
            browser.path,
            "--profile",
            str(profile),
            "--new-instance",
            "--name",
            WINDOW_CLASS,
            "--class",
            WINDOW_CLASS,
            APPLE_TV_URL,
        ]

    ensure_profile_dir(profile)
    return [
        browser.path,
        f"--user-data-dir={profile}",
        f"--app={APPLE_TV_URL}",
        f"--class={WINDOW_CLASS}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-sync",
    ]


def launch(
    browser: Browser,
    *,
    profile: Path,
    hardware_decode: bool = False,
    replace_process: bool = False,
) -> subprocess.Popen[bytes] | None:
    command = build_command(
        browser,
        profile=profile,
        hardware_decode=hardware_decode,
    )
    if replace_process:
        os.execv(command[0], command)
    return subprocess.Popen(command, start_new_session=True)
