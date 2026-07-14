"""Product listing and sorting scenarios (Selenium)."""

from __future__ import annotations

import allure
import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from tests.base_test import BaseTest


@allure.epic("Sauce Demo")
@allure.feature("Products")
@pytest.mark.ui
@pytest.mark.products
class TestProducts(BaseTest):
    """Inventory listing and sort order validations."""

    @pytest.fixture(autouse=True)
    def _login(self, driver) -> None:
        LoginPage(driver).open_login().login_as_standard_user()
        InventoryPage(driver).wait_until_loaded()

    @pytest.mark.smoke
    @pytest.mark.sanity
    def test_product_listing(self, driver, test_data) -> None:
        inventory = InventoryPage(driver)
        names = inventory.get_product_names()
        prices = inventory.get_product_prices()

        assert inventory.get_product_count() == 6
        assert len(names) == 6
        assert len(prices) == 6

        backpack = test_data["products"]["backpack"]
        assert backpack["name"] in names
        assert backpack["price"] in prices
        self.assert_page_url_contains(driver, "inventory.html")

    @pytest.mark.regression
    @pytest.mark.parametrize(
        "sort_key",
        ["name_a_to_z", "name_z_to_a", "price_low_to_high", "price_high_to_low"],
    )
    def test_product_sorting(self, driver, test_data, sort_key: str) -> None:
        sort_cfg = test_data["sorting"][sort_key]
        inventory = InventoryPage(driver)
        inventory.sort_products(sort_cfg["value"])

        names = inventory.get_product_names()
        prices = inventory.get_product_prices()

        self.assert_product_name(names[0], sort_cfg["first_product"])
        if "first_price" in sort_cfg:
            self.assert_product_price(prices[0], sort_cfg["first_price"])

        # Name sorts should be lexicographically ordered
        if sort_key == "name_a_to_z":
            assert names == sorted(names)
        if sort_key == "name_z_to_a":
            assert names == sorted(names, reverse=True)
