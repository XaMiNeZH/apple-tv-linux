"""Build and run a dedicated tv.apple.com browser window."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from tvweb import APPLE_TV_URL, WINDOW_CLASS
from tvweb.browsers import Browser

CHROMIUM_VAAPI_ENABLE = (
    "VaapiVideoDecodeLinuxGL,VaapiIgnoreDriverChecks,AcceleratedVideoDecodeLinuxGL"
)
CHROMIUM_VAAPI_DISABLE = "UseChromeOSDirectVideoDecoder"

FIREFOX_USER_JS = """\
// Written by TV Web for this dedicated profile.
user_pref("media.ffmpeg.vaapi.enabled", {vaapi});
user_pref("browser.tabs.warnOnClose", false);
user_pref("browser.sessionstore.resume_from_crash", false);
"""


def ensure_profile_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_firefox_user_js(profile: Path, hardware_decode: bool) -> None:
    ensure_profile_dir(profile)
    (profile / "user.js").write_text(
        FIREFOX_USER_JS.format(vaapi="true" if hardware_decode else "false"),
        encoding="utf-8",
    )


def build_command(
    browser: Browser,
    *,
    profile: Path,
    hardware_decode: bool,
) -> list[str]:
    if browser.kind == "firefox":
        write_firefox_user_js(profile, hardware_decode)
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
    command = [
        browser.path,
        f"--user-data-dir={profile}",
        f"--app={APPLE_TV_URL}",
        f"--class={WINDOW_CLASS}",
        "--ozone-platform-hint=auto",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-sync",
    ]
    if hardware_decode:
        command.extend(
            [
                f"--enable-features={CHROMIUM_VAAPI_ENABLE}",
                f"--disable-features={CHROMIUM_VAAPI_DISABLE}",
            ]
        )
    return command


def launch(
    browser: Browser,
    *,
    profile: Path,
    hardware_decode: bool,
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
