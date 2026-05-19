"""
SauceDemo Login Page — Page Object.
Encapsulates element locators and actions for the login page.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for SauceDemo login page."""

    BASE_URL = "https://www.saucedemo.com"

    # Element locators
    USERNAME    = (By.ID, "user-name")
    PASSWORD    = (By.ID, "password")
    BTN_LOGIN   = (By.ID, "login-button")
    ERROR_MSG   = (By.CSS_SELECTOR, "h3[data-test='error']")
    ERROR_CLOSE = (By.CSS_SELECTOR, "button.error-button")

    def open_login_page(self):
        return self.open()

    def login(self, username, password):
        """Fill credentials and click login."""
        self.type_text(self.USERNAME, username)
        self.type_text(self.PASSWORD, password)
        self.click(self.BTN_LOGIN)
        return self

    def is_error_visible(self):
        return self.is_visible(self.ERROR_MSG, timeout=5)

    def get_error(self):
        return self.get_text(self.ERROR_MSG)

    def close_error(self):
        self.click(self.ERROR_CLOSE)
        return self
