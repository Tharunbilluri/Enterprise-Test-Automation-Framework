"""Login page object for Sauce Demo (Selenium)."""

from __future__ import annotations

from locators import login_locators as loc
from pages.base_page import BasePage
from utils.logger_util import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):
    """Actions and validations for the Sauce Demo login screen."""

    def open_login(self) -> "LoginPage":
        """Navigate to the login page."""
        self.open("")
        self.wait.for_visible(loc.LOGIN_BUTTON)
        return self

    def enter_username(self, username: str) -> "LoginPage":
        """Enter username."""
        self.type_text(loc.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        """Enter password."""
        self.type_text(loc.PASSWORD_INPUT, password)
        return self

    def click_login(self) -> None:
        """Submit the login form."""
        self.click(loc.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        """Complete a full login attempt."""
        logger.info("Attempting login as '%s'", username)
        self.enter_username(username).enter_password(password).click_login()

    def login_as_standard_user(self) -> None:
        """Log in with configured valid credentials."""
        self.login(self.settings.valid_username, self.settings.valid_password)

    def get_error_message(self) -> str:
        """Return the login error banner text."""
        return self.get_text(loc.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        """Return True when the error banner is visible."""
        return self.is_displayed(loc.ERROR_MESSAGE)

    def is_on_login_page(self) -> bool:
        """Return True when the login button is visible."""
        return self.is_displayed(loc.LOGIN_BUTTON)
