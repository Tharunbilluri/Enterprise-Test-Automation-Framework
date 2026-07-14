"""Cart page locators for Sauce Demo."""

from __future__ import annotations

from selenium.webdriver.common.by import By

CART_LIST = (By.CSS_SELECTOR, "[data-test='cart-list']")
CART_ITEM = (By.CSS_SELECTOR, "[data-test='inventory-item']")
CART_ITEM_NAME = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
CART_ITEM_PRICE = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
CHECKOUT_BUTTON = (By.CSS_SELECTOR, "[data-test='checkout']")
CONTINUE_SHOPPING = (By.CSS_SELECTOR, "[data-test='continue-shopping']")
TITLE = (By.CSS_SELECTOR, "[data-test='title']")
SHOPPING_CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")


def remove_button(product_slug: str) -> tuple[str, str]:
    """Build remove button locator on the cart page."""
    return (By.CSS_SELECTOR, f"[data-test='remove-{product_slug}']")
