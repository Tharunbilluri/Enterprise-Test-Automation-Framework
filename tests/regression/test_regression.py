"""Regression suite entry — broad tagged scenarios."""

from __future__ import annotations

import allure
import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from tests.base_test import BaseTest


@allure.epic("Sauce Demo")
@allure.feature("Regression")
@pytest.mark.regression
@pytest.mark.ui
class TestRegressionSanity(BaseTest):
    """Additional regression checks beyond smoke."""

    def test_inventory_title_and_url_after_login(self, driver, settings) -> None:
        LoginPage(driver).open_login().login_as_standard_user()
        inventory = InventoryPage(driver).wait_until_loaded()

        self.assert_page_title(driver, settings.base_title)
        self.assert_page_url_contains(driver, "inventory.html")
        assert inventory.get_page_heading() == "Products"
        assert inventory.get_product_count() >= 1
