"""Login and logout scenarios (Selenium)."""

from __future__ import annotations

import allure
import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from tests.base_test import BaseTest


@allure.epic("Sauce Demo")
@allure.feature("Authentication")
@pytest.mark.ui
@pytest.mark.login
class TestLogin(BaseTest):
    """Valid, invalid, and logout coverage."""

    @pytest.mark.smoke
    @pytest.mark.sanity
    def test_login_with_valid_credentials(self, driver, test_data, settings) -> None:
        creds = test_data["valid_login"]
        login = LoginPage(driver).open_login()
        login.login(creds["username"], creds["password"])

        InventoryPage(driver).wait_until_loaded()
        self.assert_page_url_contains(driver, "inventory")
        self.assert_page_title(driver, settings.base_title)

    @pytest.mark.regression
    @pytest.mark.parametrize(
        "case",
        [
            pytest.param("wrong_password", id="wrong_password"),
            pytest.param("wrong_username", id="wrong_username"),
            pytest.param("locked_out_user", id="locked_out_user"),
        ],
    )
    def test_invalid_login(self, driver, test_data, case: str) -> None:
        row = next(item for item in test_data["invalid_login"] if item["case"] == case)
        login = LoginPage(driver).open_login()
        login.login(row["username"], row["password"])

        assert login.is_error_displayed()
        self.assert_error_message(login.get_error_message(), row["expected_error"])
        self.assert_page_url_contains(driver, "saucedemo.com")
        assert "inventory" not in driver.current_url

    @pytest.mark.regression
    @pytest.mark.sanity
    def test_logout(self, driver) -> None:
        login = LoginPage(driver).open_login()
        login.login_as_standard_user()

        inventory = InventoryPage(driver).wait_until_loaded()
        inventory.logout()

        assert LoginPage(driver).is_on_login_page()
        self.assert_page_url_contains(driver, "saucedemo.com")
        assert "inventory" not in driver.current_url
