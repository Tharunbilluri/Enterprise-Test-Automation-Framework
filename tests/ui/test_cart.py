"""Cart add/remove scenarios (Selenium)."""

from __future__ import annotations

import allure
import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from tests.base_test import BaseTest


@allure.epic("Sauce Demo")
@allure.feature("Cart")
@pytest.mark.ui
@pytest.mark.cart
class TestCart(BaseTest):
    """Add to cart and remove from cart coverage."""

    @pytest.fixture(autouse=True)
    def _login(self, driver) -> None:
        LoginPage(driver).open_login().login_as_standard_user()
        InventoryPage(driver).wait_until_loaded()

    @pytest.mark.smoke
    def test_add_to_cart(self, driver, test_data) -> None:
        product = test_data["products"]["backpack"]
        inventory = InventoryPage(driver)
        inventory.add_to_cart(product["name"])

        self.assert_cart_count(inventory.get_cart_count(), 1)
        inventory.open_cart()

        cart = CartPage(driver).wait_until_loaded()
        assert cart.get_item_count() == 1
        self.assert_product_name(cart.get_item_names()[0], product["name"])
        self.assert_product_price(cart.get_item_prices()[0], product["price"])

    @pytest.mark.regression
    def test_add_multiple_products_to_cart(self, driver, test_data) -> None:
        backpack = test_data["products"]["backpack"]
        bike = test_data["products"]["bike_light"]
        inventory = InventoryPage(driver)
        inventory.add_to_cart(backpack["name"]).add_to_cart(bike["name"])

        self.assert_cart_count(inventory.get_cart_count(), 2)
        inventory.open_cart()

        cart = CartPage(driver).wait_until_loaded()
        names = cart.get_item_names()
        assert backpack["name"] in names
        assert bike["name"] in names
        assert cart.get_item_count() == 2

    @pytest.mark.regression
    def test_remove_from_cart_on_inventory(self, driver, test_data) -> None:
        product = test_data["products"]["backpack"]
        inventory = InventoryPage(driver)
        inventory.add_to_cart(product["name"])
        self.assert_cart_count(inventory.get_cart_count(), 1)

        inventory.remove_from_cart(product["name"])
        self.assert_cart_count(inventory.get_cart_count(), 0)

    @pytest.mark.regression
    def test_remove_from_cart_page(self, driver, test_data) -> None:
        product = test_data["products"]["onesie"]
        inventory = InventoryPage(driver)
        inventory.add_to_cart(product["name"])
        inventory.open_cart()

        cart = CartPage(driver).wait_until_loaded()
        cart.remove_item(product["name"])
        assert cart.get_item_count() == 0
