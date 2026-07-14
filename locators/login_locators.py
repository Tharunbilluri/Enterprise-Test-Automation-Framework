"""Login page locators for Sauce Demo."""

from __future__ import annotations

from selenium.webdriver.common.by import By

USERNAME_INPUT = (By.CSS_SELECTOR, "[data-test='username']")
PASSWORD_INPUT = (By.CSS_SELECTOR, "[data-test='password']")
LOGIN_BUTTON = (By.CSS_SELECTOR, "[data-test='login-button']")
ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
LOGIN_LOGO = (By.CLASS_NAME, "login_logo")
