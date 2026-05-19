"""
DEBIM (Near East University Distance Learning) Login Page Object.
This file demonstrates the framework's portability — adapted to a new site.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class DebimLoginPage(BasePage):
    """Page Object for DEBİM login page."""

    BASE_URL = "https://debim.neu.edu.tr"

    USERNAME   = (By.ID, "inputName")
    PASSWORD   = (By.ID, "inputPassword")
    BTN_SUBMIT = (By.ID, "submit")
    ERROR_MSG  = (By.CSS_SELECTOR, ".alert-danger, .loginerrors, #loginerrormessage")

    def open_login_page(self):
        self.open()
        return self

    def login(self, username, password):
        # Wait until page is loaded
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self.USERNAME)
        )
        username_field = self.driver.find_element(*self.USERNAME)
        password_field = self.driver.find_element(*self.PASSWORD)
        username_field.clear()
        username_field.send_keys(username)
        password_field.clear()
        password_field.send_keys(password)
        self.driver.find_element(*self.BTN_SUBMIT).click()
        return self

    def is_on_login_page(self):
        return "debim" in self.current_url().lower()

    def get_page_title(self):
        return self.driver.title

    def is_username_field_present(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.USERNAME)
            )
            return True
        except Exception:
            return False

    def is_password_field_present(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.PASSWORD)
            )
            return True
        except Exception:
            return False

    def is_login_button_present(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.BTN_SUBMIT)
            )
            return True
        except Exception:
            return False

    def is_error_visible(self):
        return self.is_visible(self.ERROR_MSG, timeout=5)
