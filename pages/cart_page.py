"""Cart page object for Sauce Demo (Selenium)."""

from __future__ import annotations

from locators import cart_locators as loc
from pages.base_page import BasePage
from pages.inventory_page import PRODUCT_SLUGS
from utils.logger_util import get_logger

logger = get_logger(__name__)


class CartPage(BasePage):
    """Cart review, remove item, and proceed to checkout."""

    def wait_until_loaded(self) -> "CartPage":
        """Wait until cart page is ready."""
        self.wait_for_url_contains("cart")
        self.wait.for_visible(loc.CART_LIST)
        return self

    def get_page_heading(self) -> str:
        """Return cart page heading."""
        return self.get_text(loc.TITLE)

    def get_item_names(self) -> list[str]:
        """Return product names currently in the cart."""
        elements = self.driver.find_elements(*loc.CART_ITEM_NAME)
        return [el.text.strip() for el in elements]

    def get_item_prices(self) -> list[str]:
        """Return product prices currently in the cart."""
        elements = self.driver.find_elements(*loc.CART_ITEM_PRICE)
        return [el.text.strip() for el in elements]

    def get_item_count(self) -> int:
        """Return count of line items in the cart."""
        return len(self.driver.find_elements(*loc.CART_ITEM))

    def remove_item(self, product_name: str) -> "CartPage":
        """Remove a line item by product display name."""
        slug = PRODUCT_SLUGS[product_name]
        logger.info("Removing from cart page: %s", product_name)
        self.click(loc.remove_button(slug))
        return self

    def proceed_to_checkout(self) -> None:
        """Click Checkout."""
        self.click(loc.CHECKOUT_BUTTON)

    def continue_shopping(self) -> None:
        """Return to inventory."""
        self.click(loc.CONTINUE_SHOPPING)
