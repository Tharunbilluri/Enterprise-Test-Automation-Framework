"""Shared assertion helpers for URL, title, and text validations."""

from __future__ import annotations

from typing import Any

from utils.logger_util import get_logger

logger = get_logger(__name__)


def assert_url_contains(current_url: str, expected_fragment: str) -> None:
    """Assert that ``current_url`` contains ``expected_fragment``."""
    assert expected_fragment in current_url, (
        f"Expected URL to contain '{expected_fragment}', got '{current_url}'"
    )
    logger.debug("URL assertion passed: contains '%s'", expected_fragment)


def assert_title_equals(actual_title: str, expected_title: str) -> None:
    """Assert exact page title match."""
    assert actual_title == expected_title, (
        f"Expected title '{expected_title}', got '{actual_title}'"
    )
    logger.debug("Title assertion passed: '%s'", expected_title)


def assert_text_equals(actual: str, expected: str, *, field: str = "text") -> None:
    """Assert normalized string equality."""
    actual_norm = (actual or "").strip()
    expected_norm = (expected or "").strip()
    assert actual_norm == expected_norm, (
        f"Expected {field} '{expected_norm}', got '{actual_norm}'"
    )


def assert_text_contains(actual: str, expected_substring: str, *, field: str = "text") -> None:
    """Assert that ``actual`` contains ``expected_substring``."""
    assert expected_substring in (actual or ""), (
        f"Expected {field} to contain '{expected_substring}', got '{actual}'"
    )


def assert_count_equals(actual: int, expected: int, *, field: str = "count") -> None:
    """Assert integer equality for cart badges, list lengths, etc."""
    assert actual == expected, f"Expected {field}={expected}, got {actual}"


def attach_allure_text(name: str, body: str) -> None:
    """Attach plain text to Allure when the library is available."""
    try:
        import allure

        allure.attach(
            body,
            name=name,
            attachment_type=allure.attachment_type.TEXT,
        )
    except Exception:  # noqa: BLE001 — Allure is optional at import time
        logger.debug("Allure not available; skipped attachment '%s'", name)


def attach_allure_png(name: str, png_bytes: bytes) -> None:
    """Attach a PNG screenshot to Allure when available."""
    try:
        import allure

        allure.attach(
            png_bytes,
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception:  # noqa: BLE001
        logger.debug("Allure not available; skipped PNG '%s'", name)


def safe_getattr(obj: Any, attr: str, default: Any = None) -> Any:
    """Return attribute value or default without raising."""
    return getattr(obj, attr, default)
