"""Checkout and complete purchase scenarios (Selenium)."""

from __future__ import annotations

import allure
import pytest
from faker import Faker

from pages.cart_page import CartPage
from pages.checkout_page import (
    CheckoutCompletePage,
    CheckoutStepOnePage,
    CheckoutStepTwoPage,
)
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from tests.base_test import BaseTest

fake = Faker()


@allure.epic("Sauce Demo")
@allure.feature("Checkout")
@pytest.mark.ui
@pytest.mark.cart
@pytest.mark.regression
class TestCheckout(BaseTest):
    """End-to-end checkout validations."""

    def _login_and_add(self, driver, product_name: str) -> InventoryPage:
        LoginPage(driver).open_login().login_as_standard_user()
        inventory = InventoryPage(driver).wait_until_loaded()
        inventory.add_to_cart(product_name)
        return inventory

    def test_checkout_complete_purchase(self, driver, test_data) -> None:
        product = test_data["products"]["fleece"]
        checkout = test_data["checkout"]

        inventory = self._login_and_add(driver, product["name"])
        self.assert_cart_count(inventory.get_cart_count(), 1)
        inventory.open_cart()

        CartPage(driver).wait_until_loaded().proceed_to_checkout()

        step_one = CheckoutStepOnePage(driver).wait_until_loaded()
        step_one.fill_customer_info(
            checkout["first_name"],
            checkout["last_name"],
            checkout["postal_code"],
        ).continue_to_overview()

        step_two = CheckoutStepTwoPage(driver).wait_until_loaded()
        self.assert_product_name(step_two.get_item_names()[0], product["name"])
        self.assert_product_price(step_two.get_item_prices()[0], product["price"])
        assert "Total:" in step_two.get_total_label()
        step_two.finish()

        complete = CheckoutCompletePage(driver).wait_until_loaded()
        assert complete.get_complete_header() == checkout["success_header"]
        self.assert_page_url_contains(driver, "checkout-complete.html")

    def test_checkout_with_faker_customer_data(self, driver, test_data) -> None:
        product = test_data["products"]["bike_light"]
        inventory = self._login_and_add(driver, product["name"])
        inventory.open_cart()
        CartPage(driver).wait_until_loaded().proceed_to_checkout()

        CheckoutStepOnePage(driver).wait_until_loaded().fill_customer_info(
            fake.first_name(),
            fake.last_name(),
            fake.postcode(),
        ).continue_to_overview()

        CheckoutStepTwoPage(driver).wait_until_loaded().finish()
        complete = CheckoutCompletePage(driver).wait_until_loaded()
        assert "Thank you" in complete.get_complete_header()
