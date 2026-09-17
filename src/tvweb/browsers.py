"""Detect DRM-capable browsers on Fedora."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from typing import Literal

BrowserKind = Literal["chromium", "firefox"]


@dataclass(frozen=True)
class Browser:
    id: str
    name: str
    kind: BrowserKind
    path: str
    drm_likely: bool


# Preference order: browsers that ship Widevine on Fedora first.
_CANDIDATES: tuple[tuple[str, str, BrowserKind, bool], ...] = (
    ("google-chrome-stable", "Google Chrome", "chromium", True),
    ("google-chrome", "Google Chrome", "chromium", True),
    ("microsoft-edge-stable", "Microsoft Edge", "chromium", True),
    ("microsoft-edge", "Microsoft Edge", "chromium", True),
    ("firefox", "Firefox", "firefox", True),
    ("chromium-browser", "Chromium", "chromium", False),
    ("chromium", "Chromium", "chromium", False),
)


def detect_browsers(path: str | None = None) -> list[Browser]:
    """Return installed browsers, best DRM prospects first.

    Distro Chromium is last: Fedora's package often has no Widevine CDM,
    so tv.apple.com will fail to play until Chrome, Edge, or Firefox is used.
    """
    found: list[Browser] = []
    seen_paths: set[str] = set()
    for binary, name, kind, drm_likely in _CANDIDATES:
        resolved = shutil.which(binary, path=path)
        if not resolved:
            continue
        if resolved in seen_paths:
            continue
        seen_paths.add(resolved)
        found.append(
            Browser(
                id=binary,
                name=name,
                kind=kind,
                path=resolved,
                drm_likely=drm_likely,
            )
        )
    return found


def browser_by_id(browsers: list[Browser], browser_id: str | None) -> Browser | None:
    if not browser_id:
        return None
    for browser in browsers:
        if browser.id == browser_id:
            return browser
    return None


def pick_browser(browsers: list[Browser], preferred_id: str | None = None) -> Browser | None:
    chosen = browser_by_id(browsers, preferred_id)
    if chosen:
        return chosen
    return browsers[0] if browsers else None
