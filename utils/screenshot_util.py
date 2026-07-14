"""Screenshot capture helpers for Selenium and Playwright."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from config.settings import get_settings
from utils.file_util import ensure_directory, sanitize_filename, timestamp_slug
from utils.logger_util import get_logger

logger = get_logger(__name__)


def _screenshot_path(name: str, destination: Path | None = None) -> Path:
    settings = get_settings()
    folder = ensure_directory(destination or settings.screenshots_dir)
    safe_name = sanitize_filename(name)
    return folder / f"{safe_name}_{timestamp_slug()}.png"


def capture_selenium_screenshot(
    driver: Any,
    name: str,
    destination: Path | None = None,
) -> Path | None:
    """
    Capture a full-window Selenium screenshot.

    Returns the file path on success, or ``None`` if capture fails.
    """
    path = _screenshot_path(name, destination)
    try:
        success = driver.save_screenshot(str(path))
        if not success:
            logger.warning("Selenium reported unsuccessful screenshot: %s", path)
            return None
        logger.info("Screenshot saved: %s", path)
        return path
    except Exception as exc:  # noqa: BLE001 — must not mask original test failure
        logger.error("Failed to capture Selenium screenshot '%s': %s", name, exc)
        return None


def capture_playwright_screenshot(
    page: Any,
    name: str,
    destination: Path | None = None,
    *,
    full_page: bool = True,
) -> Path | None:
    """Capture a Playwright page screenshot."""
    path = _screenshot_path(name, destination)
    try:
        page.screenshot(path=str(path), full_page=full_page)
        logger.info("Screenshot saved: %s", path)
        return path
    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to capture Playwright screenshot '%s': %s", name, exc)
        return None


def capture_failure_screenshot(
    driver_or_page: Any,
    test_name: str,
    *,
    engine: str | None = None,
) -> Path | None:
    """
    Capture a failure screenshot using the configured or provided engine.

    ``driver_or_page`` should be a Selenium WebDriver or Playwright Page.
    """
    settings = get_settings()
    if not settings.screenshot_on_failure:
        logger.debug("Screenshot on failure disabled; skipping.")
        return None

    resolved_engine = (engine or settings.automation_engine).lower()
    artifact_name = f"FAIL_{test_name}"

    if resolved_engine == "playwright":
        return capture_playwright_screenshot(driver_or_page, artifact_name)
    return capture_selenium_screenshot(driver_or_page, artifact_name)
