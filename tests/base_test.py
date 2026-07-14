"""Reusable BaseTest helpers shared across UI suites."""

from __future__ import annotations

from typing import Any

from config.settings import Settings, get_settings
from utils.assert_util import (
    assert_count_equals,
    assert_text_contains,
    assert_text_equals,
    assert_title_equals,
    assert_url_contains,
)
from utils.logger_util import get_logger

logger = get_logger(__name__)


class BaseTest:
    """
    Lightweight test foundation for common validations and settings access.

    Driver/page lifecycle remains in ``conftest.py`` fixtures (composition over
    deep inheritance). Suites inherit ``BaseTest`` for shared assertion helpers
    and credentials — a pattern expected in many enterprise SDET codebases.
    """

    @property
    def settings(self) -> Settings:
        """Return cached framework settings."""
        return get_settings()

    def assert_page_url_contains(self, driver_or_page: Any, fragment: str) -> None:
        """Validate URL fragment for Selenium driver or Playwright page."""
        url = self._resolve_url(driver_or_page)
        assert_url_contains(url, fragment)
        logger.info("Validated URL contains '%s'", fragment)

    def assert_page_title(self, driver_or_page: Any, expected_title: str | None = None) -> None:
        """Validate document title."""
        expected = expected_title or self.settings.base_title
        title = self._resolve_title(driver_or_page)
        assert_title_equals(title, expected)
        logger.info("Validated title == '%s'", expected)

    def assert_error_message(self, actual: str, expected_substring: str) -> None:
        """Validate an error banner/message contains expected text."""
        assert_text_contains(actual, expected_substring, field="error message")

    def assert_cart_count(self, actual: int, expected: int) -> None:
        """Validate cart badge count."""
        assert_count_equals(actual, expected, field="cart count")

    def assert_product_name(self, actual: str, expected: str) -> None:
        """Validate product display name."""
        assert_text_equals(actual, expected, field="product name")

    def assert_product_price(self, actual: str, expected: str) -> None:
        """Validate product price string (e.g. ``$29.99``)."""
        assert_text_equals(actual, expected, field="product price")

    @staticmethod
    def _resolve_url(driver_or_page: Any) -> str:
        if hasattr(driver_or_page, "current_url"):
            return str(driver_or_page.current_url)
        if hasattr(driver_or_page, "url"):
            return str(driver_or_page.url)
        raise TypeError("Unsupported driver/page type for URL resolution")

    @staticmethod
    def _resolve_title(driver_or_page: Any) -> str:
        title = getattr(driver_or_page, "title", None)
        if callable(title):
            return str(title())  # Playwright: page.title()
        if isinstance(title, str):
            return title  # Selenium: driver.title
        raise TypeError("Unsupported driver/page type for title resolution")
