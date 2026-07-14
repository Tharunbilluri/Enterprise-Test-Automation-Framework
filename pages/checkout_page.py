"""Checkout page objects for Sauce Demo (Selenium)."""

from __future__ import annotations

from locators import checkout_locators as loc
from pages.base_page import BasePage
from utils.logger_util import get_logger

logger = get_logger(__name__)


class CheckoutStepOnePage(BasePage):
    """Checkout step one — customer information."""

    def wait_until_loaded(self) -> "CheckoutStepOnePage":
        """Wait until checkout step one is ready."""
        self.wait_for_url_contains("checkout-step-one")
        self.wait.for_visible(loc.FIRST_NAME)
        return self

    def fill_customer_info(
        self,
        first_name: str,
        last_name: str,
        postal_code: str,
    ) -> "CheckoutStepOnePage":
        """Fill first name, last name, and postal code."""
        logger.info("Filling checkout customer info")
        self.type_text(loc.FIRST_NAME, first_name)
        self.type_text(loc.LAST_NAME, last_name)
        self.type_text(loc.POSTAL_CODE, postal_code)
        return self

    def continue_to_overview(self) -> None:
        """Proceed to checkout overview."""
        self.click(loc.CONTINUE_BUTTON)

    def get_error_message(self) -> str:
        """Return checkout form error text."""
        return self.get_text(loc.ERROR_MESSAGE)


class CheckoutStepTwoPage(BasePage):
    """Checkout step two — order overview."""

    def wait_until_loaded(self) -> "CheckoutStepTwoPage":
        """Wait until overview is ready."""
        self.wait_for_url_contains("checkout-step-two")
        self.wait.for_visible(loc.FINISH_BUTTON)
        return self

    def get_item_names(self) -> list[str]:
        """Return item names on the overview."""
        return [el.text.strip() for el in self.find_all(loc.OVERVIEW_ITEM_NAME)]

    def get_item_prices(self) -> list[str]:
        """Return item prices on the overview."""
        return [el.text.strip() for el in self.find_all(loc.OVERVIEW_ITEM_PRICE)]

    def get_total_label(self) -> str:
        """Return the total label text."""
        return self.get_text(loc.SUMMARY_TOTAL)

    def finish(self) -> None:
        """Complete the purchase."""
        logger.info("Finishing checkout")
        self.click(loc.FINISH_BUTTON)


class CheckoutCompletePage(BasePage):
    """Checkout complete — order confirmation."""

    def wait_until_loaded(self) -> "CheckoutCompletePage":
        """Wait until confirmation page is ready."""
        self.wait_for_url_contains("checkout-complete")
        self.wait.for_visible(loc.COMPLETE_HEADER)
        return self

    def get_complete_header(self) -> str:
        """Return the success header text."""
        return self.get_text(loc.COMPLETE_HEADER)

    def get_complete_text(self) -> str:
        """Return the success body text."""
        return self.get_text(loc.COMPLETE_TEXT)

    def back_to_products(self) -> None:
        """Navigate back to inventory."""
        self.click(loc.BACK_HOME)
