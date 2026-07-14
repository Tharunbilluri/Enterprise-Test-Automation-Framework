"""Browser capability helpers derived from Settings."""

from __future__ import annotations

from typing import Any

from config.settings import Settings, get_settings


SUPPORTED_BROWSERS: frozenset[str] = frozenset({"chrome", "edge", "firefox"})
SUPPORTED_ENGINES: frozenset[str] = frozenset({"selenium", "playwright"})


def validate_browser(browser: str) -> str:
    """Normalize and validate browser name."""
    normalized = browser.strip().lower()
    if normalized not in SUPPORTED_BROWSERS:
        allowed = ", ".join(sorted(SUPPORTED_BROWSERS))
        raise ValueError(f"Unsupported browser '{browser}'. Allowed: {allowed}")
    return normalized


def validate_engine(engine: str) -> str:
    """Normalize and validate automation engine."""
    normalized = engine.strip().lower()
    if normalized not in SUPPORTED_ENGINES:
        allowed = ", ".join(sorted(SUPPORTED_ENGINES))
        raise ValueError(f"Unsupported engine '{engine}'. Allowed: {allowed}")
    return normalized


def selenium_common_args(settings: Settings | None = None) -> dict[str, Any]:
    """
    Return shared Selenium launch arguments.

    Used by browser factory utilities (Step 4+) to keep driver creation DRY.
    """
    cfg = settings or get_settings()
    browser = validate_browser(cfg.browser)
    return {
        "browser": browser,
        "headless": cfg.headless,
        "window_width": cfg.window_width,
        "window_height": cfg.window_height,
        "page_load_timeout": cfg.page_load_timeout,
        "implicit_wait": cfg.implicit_wait,
        "explicit_wait": cfg.explicit_wait,
    }


def playwright_common_args(settings: Settings | None = None) -> dict[str, Any]:
    """Return shared Playwright launch arguments."""
    cfg = settings or get_settings()
    browser = validate_browser(cfg.browser)
    return {
        "browser": browser,
        "headless": cfg.headless,
        "viewport": {
            "width": cfg.window_width,
            "height": cfg.window_height,
        },
        "base_url": cfg.base_url,
    }
