"""Playwright engine smoke tests for Sauce Demo."""

from __future__ import annotations

import allure
import pytest

from pages.playwright_pages import (
    PlaywrightCartPage,
    PlaywrightCheckoutPages,
    PlaywrightInventoryPage,
    PlaywrightLoginPage,
)
from tests.base_test import BaseTest


@allure.epic("Sauce Demo")
@allure.feature("Playwright")
@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.login
@pytest.mark.playwright
class TestPlaywrightSmoke(BaseTest):
    """Requires ``--engine=playwright`` (or AUTOMATION_ENGINE=playwright)."""

    def test_playwright_login(self, page, settings) -> None:
        login = PlaywrightLoginPage(page).open_login()
        login.login_as_standard_user()
        inventory = PlaywrightInventoryPage(page).wait_until_loaded()

        self.assert_page_url_contains(page, "inventory")
        self.assert_page_title(page, settings.base_title)
        assert len(inventory.get_product_names()) == 6

    def test_playwright_checkout(self, page, test_data) -> None:
        product = test_data["products"]["backpack"]
        checkout = test_data["checkout"]

        PlaywrightLoginPage(page).open_login().login_as_standard_user()
        inventory = PlaywrightInventoryPage(page).wait_until_loaded()
        inventory.add_to_cart(product["name"])
        self.assert_cart_count(inventory.get_cart_count(), 1)
        inventory.open_cart()

        PlaywrightCartPage(page).wait_until_loaded().proceed_to_checkout()
        checkout_pages = PlaywrightCheckoutPages(page)
        checkout_pages.fill_and_continue(
            checkout["first_name"],
            checkout["last_name"],
            checkout["postal_code"],
        )
        checkout_pages.finish()
        assert checkout_pages.get_complete_header() == checkout["success_header"]
        self.assert_page_url_contains(page, "checkout-complete")
