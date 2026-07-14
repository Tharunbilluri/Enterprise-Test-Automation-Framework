"""Explicit wait helpers for Selenium (no implicit waits)."""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import get_settings
from utils.logger_util import get_logger

T = TypeVar("T")
Locator = tuple[str, str]

logger = get_logger(__name__)


class WaitUtil:
    """Thin wrapper around ``WebDriverWait`` with consistent timeouts/logging."""

    def __init__(self, driver: WebDriver, timeout: int | None = None) -> None:
        self._driver = driver
        self._timeout = timeout if timeout is not None else get_settings().explicit_wait

    @property
    def timeout(self) -> int:
        return self._timeout

    def _wait(self) -> WebDriverWait:
        return WebDriverWait(self._driver, self._timeout)

    def until(self, condition: Callable[[WebDriver], T], message: str = "") -> T:
        """Wait until a custom expected condition returns a truthy value."""
        try:
            return self._wait().until(condition, message=message)
        except TimeoutException:
            logger.error("Wait timed out after %ss: %s", self._timeout, message or condition)
            raise

    def for_visible(self, locator: Locator) -> WebElement:
        """Wait until the element located by ``locator`` is visible."""
        return self.until(
            EC.visibility_of_element_located(locator),
            message=f"Element not visible: {locator}",
        )

    def for_present(self, locator: Locator) -> WebElement:
        """Wait until the element is present in the DOM."""
        return self.until(
            EC.presence_of_element_located(locator),
            message=f"Element not present: {locator}",
        )

    def for_clickable(self, locator: Locator) -> WebElement:
        """Wait until the element is visible and enabled."""
        return self.until(
            EC.element_to_be_clickable(locator),
            message=f"Element not clickable: {locator}",
        )

    def for_invisible(self, locator: Locator) -> bool:
        """Wait until the element is invisible or detached."""
        return self.until(
            EC.invisibility_of_element_located(locator),
            message=f"Element still visible: {locator}",
        )

    def for_text_in_element(self, locator: Locator, text: str) -> bool:
        """Wait until ``text`` is present in the element."""
        return self.until(
            EC.text_to_be_present_in_element(locator, text),
            message=f"Text '{text}' not found in {locator}",
        )

    def for_url_contains(self, fragment: str) -> bool:
        """Wait until the current URL contains ``fragment``."""
        return self.until(
            EC.url_contains(fragment),
            message=f"URL did not contain '{fragment}'",
        )

    def for_title_contains(self, title_part: str) -> bool:
        """Wait until the page title contains ``title_part``."""
        return self.until(
            EC.title_contains(title_part),
            message=f"Title did not contain '{title_part}'",
        )

    def for_all_visible(self, locator: Locator) -> list[WebElement]:
        """Wait until at least one matching element is visible; return all visible."""
        self.for_visible(locator)
        return self._driver.find_elements(*locator)
