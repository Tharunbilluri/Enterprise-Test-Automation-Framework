"""Inventory / products page locators for Sauce Demo."""

from __future__ import annotations

from selenium.webdriver.common.by import By

INVENTORY_CONTAINER = (By.CSS_SELECTOR, "[data-test='inventory-container']")
INVENTORY_LIST = (By.CSS_SELECTOR, "[data-test='inventory-list']")
INVENTORY_ITEM = (By.CSS_SELECTOR, "[data-test='inventory-item']")
INVENTORY_ITEM_NAME = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
INVENTORY_ITEM_PRICE = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
PRODUCT_SORT = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
SHOPPING_CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
SHOPPING_CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
TITLE = (By.CSS_SELECTOR, "[data-test='title']")
BURGER_MENU = (By.ID, "react-burger-menu-btn")
LOGOUT_LINK = (By.CSS_SELECTOR, "[data-test='logout-sidebar-link']")
CLOSE_MENU = (By.ID, "react-burger-cross-btn")


def add_to_cart_button(product_slug: str) -> tuple[str, str]:
    """Build add-to-cart locator, e.g. ``sauce-labs-backpack``."""
    return (By.CSS_SELECTOR, f"[data-test='add-to-cart-{product_slug}']")


def remove_from_cart_button(product_slug: str) -> tuple[str, str]:
    """Build remove-from-cart locator on inventory page."""
    return (By.CSS_SELECTOR, f"[data-test='remove-{product_slug}']")
