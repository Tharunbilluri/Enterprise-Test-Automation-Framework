"""Inventory (products) page object for Sauce Demo (Selenium)."""

from __future__ import annotations

from locators import inventory_locators as loc
from pages.base_page import BasePage
from utils.logger_util import get_logger

logger = get_logger(__name__)

# Common Sauce Demo product slugs used in data-test attributes
PRODUCT_SLUGS = {
    "Sauce Labs Backpack": "sauce-labs-backpack",
    "Sauce Labs Bike Light": "sauce-labs-bike-light",
    "Sauce Labs Bolt T-Shirt": "sauce-labs-bolt-t-shirt",
    "Sauce Labs Fleece Jacket": "sauce-labs-fleece-jacket",
    "Sauce Labs Onesie": "sauce-labs-onesie",
    "Test.allTheThings() T-Shirt (Red)": "test.allthethings()-t-shirt-(red)",
}


class InventoryPage(BasePage):
    """Product listing, cart badge, sort, and logout actions."""

    def wait_until_loaded(self) -> "InventoryPage":
        """Wait until the inventory container is visible."""
        self.wait.for_visible(loc.INVENTORY_CONTAINER)
        self.wait_for_url_contains("inventory")
        return self

    def get_page_heading(self) -> str:
        """Return the inventory page heading (Products)."""
        return self.get_text(loc.TITLE)

    def get_product_names(self) -> list[str]:
        """Return all visible product names in current sort order."""
        elements = self.find_all(loc.INVENTORY_ITEM_NAME)
        return [el.text.strip() for el in elements]

    def get_product_prices(self) -> list[str]:
        """Return all visible product prices in current sort order."""
        elements = self.find_all(loc.INVENTORY_ITEM_PRICE)
        return [el.text.strip() for el in elements]

    def get_product_count(self) -> int:
        """Return number of inventory items."""
        return len(self.find_all(loc.INVENTORY_ITEM))

    def add_to_cart(self, product_name: str) -> "InventoryPage":
        """Add a product to the cart by display name."""
        slug = PRODUCT_SLUGS[product_name]
        logger.info("Adding to cart: %s", product_name)
        self.click(loc.add_to_cart_button(slug))
        return self

    def remove_from_cart(self, product_name: str) -> "InventoryPage":
        """Remove a product from the cart from the inventory page."""
        slug = PRODUCT_SLUGS[product_name]
        logger.info("Removing from cart (inventory): %s", product_name)
        self.click(loc.remove_from_cart_button(slug))
        return self

    def get_cart_count(self) -> int:
        """Return shopping cart badge count (0 when badge absent)."""
        badges = self.driver.find_elements(*loc.SHOPPING_CART_BADGE)
        if not badges:
            return 0
        return int(badges[0].text.strip())

    def open_cart(self) -> None:
        """Navigate to the cart page via the cart icon."""
        self.click(loc.SHOPPING_CART_LINK)

    def sort_products(self, option_value: str) -> "InventoryPage":
        """
        Sort products using the select ``value``.

        Values: ``az``, ``za``, ``lohi``, ``hilo``.
        """
        logger.info("Sorting products by value='%s'", option_value)
        self.select_by_value(loc.PRODUCT_SORT, option_value)
        return self

    def logout(self) -> None:
        """Open the burger menu and logout."""
        logger.info("Logging out")
        self.click(loc.BURGER_MENU)
        self.click(loc.LOGOUT_LINK)
