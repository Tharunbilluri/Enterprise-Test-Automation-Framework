"""Smoke tests — critical path for Sauce Demo (Selenium)."""

from __future__ import annotations

import allure
import pytest

from pages.cart_page import CartPage
from pages.checkout_page import (
    CheckoutCompletePage,
    CheckoutStepOnePage,
    CheckoutStepTwoPage,
)
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from tests.base_test import BaseTest


@allure.epic("Sauce Demo")
@allure.feature("Smoke")
@pytest.mark.smoke
@pytest.mark.sanity
@pytest.mark.ui
class TestSmokeFlows(BaseTest):
    """Fast critical-path coverage suitable for PR gates."""

    @allure.story("Login")
    @pytest.mark.login
    def test_valid_login(self, driver, settings) -> None:
        login = LoginPage(driver)
        login.open_login()
        login.login_as_standard_user()

        inventory = InventoryPage(driver).wait_until_loaded()
        self.assert_page_url_contains(driver, "inventory.html")
        self.assert_page_title(driver, settings.base_title)
        assert inventory.get_page_heading() == "Products"

    @allure.story("Purchase")
    @pytest.mark.cart
    def test_complete_purchase_flow(self, driver, test_data) -> None:
        product = test_data["products"]["backpack"]
        checkout = test_data["checkout"]

        login = LoginPage(driver)
        login.open_login()
        login.login_as_standard_user()

        inventory = InventoryPage(driver).wait_until_loaded()
        inventory.add_to_cart(product["name"])
        self.assert_cart_count(inventory.get_cart_count(), 1)
        inventory.open_cart()

        cart = CartPage(driver).wait_until_loaded()
        self.assert_product_name(cart.get_item_names()[0], product["name"])
        self.assert_product_price(cart.get_item_prices()[0], product["price"])
        cart.proceed_to_checkout()

        step_one = CheckoutStepOnePage(driver).wait_until_loaded()
        step_one.fill_customer_info(
            checkout["first_name"],
            checkout["last_name"],
            checkout["postal_code"],
        ).continue_to_overview()

        step_two = CheckoutStepTwoPage(driver).wait_until_loaded()
        assert product["name"] in step_two.get_item_names()
        step_two.finish()

        complete = CheckoutCompletePage(driver).wait_until_loaded()
        assert complete.get_complete_header() == checkout["success_header"]
        self.assert_page_url_contains(driver, "checkout-complete")
