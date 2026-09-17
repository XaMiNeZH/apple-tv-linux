from __future__ import annotations

from pathlib import Path

from tvweb import APPLE_TV_URL, WINDOW_CLASS
from tvweb.browsers import Browser
from tvweb.launcher import (
    CHROMIUM_VAAPI_DISABLE,
    CHROMIUM_VAAPI_ENABLE,
    build_command,
)


def _chrome(path: str = "/usr/bin/google-chrome-stable") -> Browser:
    return Browser(
        id="google-chrome-stable",
        name="Google Chrome",
        kind="chromium",
        path=path,
        drm_likely=True,
    )


def _firefox(path: str = "/usr/bin/firefox") -> Browser:
    return Browser(
        id="firefox",
        name="Firefox",
        kind="firefox",
        path=path,
        drm_likely=True,
    )


def test_chrome_app_mode_and_wayland(tmp_path: Path) -> None:
    profile = tmp_path / "chrome-profile"
    command = build_command(_chrome(), profile=profile, hardware_decode=False)
    assert command[0] == "/usr/bin/google-chrome-stable"
    assert f"--user-data-dir={profile}" in command
    assert f"--app={APPLE_TV_URL}" in command
    assert f"--class={WINDOW_CLASS}" in command
    assert "--ozone-platform-hint=auto" in command
    assert profile.is_dir()
    assert not any(part.startswith("--enable-features=") for part in command)


def test_chrome_vaapi_flags(tmp_path: Path) -> None:
    profile = tmp_path / "chrome-profile"
    command = build_command(_chrome(), profile=profile, hardware_decode=True)
    assert f"--enable-features={CHROMIUM_VAAPI_ENABLE}" in command
    assert f"--disable-features={CHROMIUM_VAAPI_DISABLE}" in command


def test_firefox_dedicated_profile(tmp_path: Path) -> None:
    profile = tmp_path / "firefox-profile"
    command = build_command(_firefox(), profile=profile, hardware_decode=True)
    assert "--app=" not in " ".join(command)
    assert command == [
        "/usr/bin/firefox",
        "--profile",
        str(profile),
        "--new-instance",
        "--name",
        WINDOW_CLASS,
        "--class",
        WINDOW_CLASS,
        APPLE_TV_URL,
    ]
    user_js = (profile / "user.js").read_text(encoding="utf-8")
    assert 'user_pref("media.ffmpeg.vaapi.enabled", true);' in user_js
