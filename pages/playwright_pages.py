"""Playwright page objects for Sauce Demo (parity with Selenium POM)."""

from __future__ import annotations

from pages.inventory_page import PRODUCT_SLUGS
from pages.playwright_base_page import PlaywrightBasePage
from utils.logger_util import get_logger

logger = get_logger(__name__)


class PlaywrightLoginPage(PlaywrightBasePage):
    """Playwright login page."""

    def open_login(self) -> "PlaywrightLoginPage":
        self.open("/")
        self.page.locator(self.data_test("login-button")).wait_for(state="visible")
        return self

    def login(self, username: str, password: str) -> None:
        logger.info("Playwright login as '%s'", username)
        self.type_text(self.data_test("username"), username)
        self.type_text(self.data_test("password"), password)
        self.click(self.data_test("login-button"))

    def login_as_standard_user(self) -> None:
        self.login(self.settings.valid_username, self.settings.valid_password)

    def get_error_message(self) -> str:
        return self.get_text(self.data_test("error"))


class PlaywrightInventoryPage(PlaywrightBasePage):
    """Playwright inventory page."""

    def wait_until_loaded(self) -> "PlaywrightInventoryPage":
        self.wait_for_url_contains("inventory")
        self.page.locator(self.data_test("inventory-container")).wait_for(
            state="visible", timeout=self.timeout_ms
        )
        return self

    def add_to_cart(self, product_name: str) -> "PlaywrightInventoryPage":
        slug = PRODUCT_SLUGS[product_name]
        self.click(self.data_test(f"add-to-cart-{slug}"))
        return self

    def get_cart_count(self) -> int:
        badge = self.page.locator(self.data_test("shopping-cart-badge"))
        if badge.count() == 0:
            return 0
        return int(badge.inner_text())

    def open_cart(self) -> None:
        self.click(self.data_test("shopping-cart-link"))

    def get_product_names(self) -> list[str]:
        return [
            t.strip()
            for t in self.page.locator(self.data_test("inventory-item-name")).all_inner_texts()
        ]

    def logout(self) -> None:
        self.click("#react-burger-menu-btn")
        self.click(self.data_test("logout-sidebar-link"))


class PlaywrightCartPage(PlaywrightBasePage):
    """Playwright cart page."""

    def wait_until_loaded(self) -> "PlaywrightCartPage":
        self.wait_for_url_contains("cart")
        return self

    def proceed_to_checkout(self) -> None:
        self.click(self.data_test("checkout"))


class PlaywrightCheckoutPages(PlaywrightBasePage):
    """Playwright checkout steps consolidated for smoke coverage."""

    def fill_and_continue(self, first: str, last: str, postal: str) -> None:
        self.type_text(self.data_test("firstName"), first)
        self.type_text(self.data_test("lastName"), last)
        self.type_text(self.data_test("postalCode"), postal)
        self.click(self.data_test("continue"))

    def finish(self) -> None:
        self.click(self.data_test("finish"))

    def get_complete_header(self) -> str:
        return self.get_text(self.data_test("complete-header"))
