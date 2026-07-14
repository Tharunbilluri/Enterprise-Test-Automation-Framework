"""Playwright Base Page Object — shared UI interactions for Playwright pages."""

from __future__ import annotations

from typing import Any

from config.settings import get_settings
from utils.logger_util import get_logger
from utils.screenshot_util import capture_playwright_screenshot

logger = get_logger(__name__)


class PlaywrightBasePage:
    """
    Reusable Page Object foundation (Playwright sync API).

    Mirrors the Selenium ``BasePage`` responsibilities so engine-specific
    page objects stay consistent for interviews and dual-stack demos.
    """

    def __init__(self, page: Any, timeout_ms: int | None = None) -> None:
        self.page = page
        self.settings = get_settings()
        self.timeout_ms = (
            timeout_ms
            if timeout_ms is not None
            else self.settings.explicit_wait * 1000
        )

    def open(self, path: str = "") -> None:
        """Navigate to ``BASE_URL`` + optional path."""
        target = path or "/"
        logger.info("Opening (Playwright): %s", target)
        self.page.goto(target, wait_until="domcontentloaded")

    def get_current_url(self) -> str:
        """Return the current page URL."""
        return self.page.url

    def get_title(self) -> str:
        """Return the current page title."""
        return self.page.title()

    def click(self, selector: str) -> None:
        """Click an element identified by Playwright selector."""
        logger.debug("Playwright click: %s", selector)
        self.page.locator(selector).click(timeout=self.timeout_ms)

    def type_text(
        self,
        selector: str,
        text: str,
        *,
        clear_first: bool = True,
    ) -> None:
        """Fill an input; clear by default."""
        locator = self.page.locator(selector)
        if clear_first:
            locator.fill(text, timeout=self.timeout_ms)
        else:
            locator.type(text, timeout=self.timeout_ms)

    def get_text(self, selector: str) -> str:
        """Return inner text for ``selector``."""
        return (self.page.locator(selector).inner_text(timeout=self.timeout_ms) or "").strip()

    def is_visible(self, selector: str) -> bool:
        """Return True if the locator is visible within the timeout."""
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=self.timeout_ms)
            return True
        except Exception:  # noqa: BLE001
            return False

    def select_option(self, selector: str, *, label: str | None = None, value: str | None = None) -> None:
        """Select a dropdown option by label or value."""
        if label is not None:
            self.page.locator(selector).select_option(label=label, timeout=self.timeout_ms)
        elif value is not None:
            self.page.locator(selector).select_option(value=value, timeout=self.timeout_ms)
        else:
            raise ValueError("Provide either label or value for select_option")

    def wait_for_url_contains(self, fragment: str) -> None:
        """Wait until the URL contains ``fragment``."""
        self.page.wait_for_url(f"**/*{fragment}*", timeout=self.timeout_ms)

    def take_screenshot(self, name: str) -> None:
        """Capture a Playwright screenshot."""
        capture_playwright_screenshot(self.page, name)

    @staticmethod
    def data_test(test_id: str) -> str:
        """Sauce Demo ``data-test`` selector helper."""
        return f"[data-test='{test_id}']"
