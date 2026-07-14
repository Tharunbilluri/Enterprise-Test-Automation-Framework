"""Selenium Base Page Object — shared UI interactions for all pages."""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

from config.settings import get_settings
from utils.logger_util import get_logger
from utils.screenshot_util import capture_selenium_screenshot
from utils.wait_util import WaitUtil

Locator = tuple[str, str]
logger = get_logger(__name__)


class BasePage:
    """
    Reusable Page Object foundation (Selenium).

    Encapsulates navigation, element interaction, and reads using explicit waits.
    Concrete pages inherit this class and expose business-level methods only.
    """

    def __init__(self, driver: WebDriver, timeout: int | None = None) -> None:
        self.driver = driver
        self.settings = get_settings()
        self.wait = WaitUtil(driver, timeout=timeout)

    # --- Navigation & page metadata -------------------------------------------------

    def open(self, path: str = "") -> None:
        """Open ``BASE_URL`` joined with an optional path."""
        base = self.settings.base_url.rstrip("/")
        suffix = path.lstrip("/")
        url = f"{base}/{suffix}" if suffix else f"{base}/"
        logger.info("Opening URL: %s", url)
        self.driver.get(url)

    def get_current_url(self) -> str:
        """Return the current browser URL."""
        return self.driver.current_url

    def get_title(self) -> str:
        """Return the current page title."""
        return self.driver.title

    def refresh(self) -> None:
        """Refresh the current page."""
        logger.debug("Refreshing page")
        self.driver.refresh()

    def navigate_back(self) -> None:
        """Navigate backward in browser history."""
        self.driver.back()

    # --- Element interactions (explicit waits) --------------------------------------

    def find(self, locator: Locator) -> WebElement:
        """Wait for visibility and return the element."""
        return self.wait.for_visible(locator)

    def find_all(self, locator: Locator) -> list[WebElement]:
        """Wait for at least one visible match and return all matches."""
        return self.wait.for_all_visible(locator)

    def click(self, locator: Locator) -> None:
        """Wait until clickable, then click."""
        logger.debug("Clicking %s", locator)
        self.wait.for_clickable(locator).click()

    def type_text(
        self,
        locator: Locator,
        text: str,
        *,
        clear_first: bool = True,
    ) -> None:
        """Type ``text`` into an input; optionally clear first."""
        element = self.wait.for_visible(locator)
        if clear_first:
            element.clear()
        logger.debug("Typing into %s", locator)
        element.send_keys(text)

    def clear(self, locator: Locator) -> None:
        """Clear an input field."""
        self.wait.for_visible(locator).clear()

    def get_text(self, locator: Locator) -> str:
        """Return visible text for ``locator``."""
        return self.wait.for_visible(locator).text.strip()

    def get_attribute(self, locator: Locator, name: str) -> str | None:
        """Return an element attribute value."""
        return self.wait.for_present(locator).get_attribute(name)

    def is_displayed(self, locator: Locator) -> bool:
        """Return True if the element becomes visible before timeout."""
        try:
            return self.wait.for_visible(locator).is_displayed()
        except Exception:  # noqa: BLE001 — presence checks should not fail the suite hard
            return False

    def is_enabled(self, locator: Locator) -> bool:
        """Return True if the element is enabled."""
        return self.wait.for_visible(locator).is_enabled()

    def select_by_visible_text(self, locator: Locator, visible_text: str) -> None:
        """Select a dropdown option by visible text."""
        element = self.wait.for_visible(locator)
        Select(element).select_by_visible_text(visible_text)
        logger.debug("Selected '%s' on %s", visible_text, locator)

    def select_by_value(self, locator: Locator, value: str) -> None:
        """Select a dropdown option by value attribute."""
        element = self.wait.for_visible(locator)
        Select(element).select_by_value(value)

    def wait_for_url_contains(self, fragment: str) -> None:
        """Block until the URL contains ``fragment``."""
        self.wait.for_url_contains(fragment)

    def wait_for_title_contains(self, title_part: str) -> None:
        """Block until the title contains ``title_part``."""
        self.wait.for_title_contains(title_part)

    def scroll_into_view(self, locator: Locator) -> None:
        """Scroll the element into the viewport via JavaScript."""
        element = self.wait.for_present(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )

    def take_screenshot(self, name: str) -> None:
        """Capture a screenshot with a business-friendly name."""
        capture_selenium_screenshot(self.driver, name)

    @staticmethod
    def by_css(selector: str) -> Locator:
        """Build a CSS locator tuple."""
        return (By.CSS_SELECTOR, selector)

    @staticmethod
    def by_id(element_id: str) -> Locator:
        """Build an ID locator tuple."""
        return (By.ID, element_id)

    @staticmethod
    def by_xpath(xpath: str) -> Locator:
        """Build an XPath locator tuple."""
        return (By.XPATH, xpath)

    @staticmethod
    def by_test_id(test_id: str) -> Locator:
        """Build a data-test locator (Sauce Demo convention)."""
        return (By.CSS_SELECTOR, f"[data-test='{test_id}']")
