"""
DEBIM Platform Tests
=====================
Automated tests for Near East University's DEBİM (Distance Learning Platform).
Demonstrates that the framework can be adapted to other websites.
"""
import pytest
import time
from pages.debim_login_page import DebimLoginPage


class TestDebim:
    """Tests DEBİM platform's basic functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Opens DEBİM page before each test."""
        self.lp = DebimLoginPage(driver)
        self.lp.open_login_page()

    def test_debim_page_loads(self):
        """
        TEST: DEBİM homepage can load.
        EXPECTED: URL contains 'debim', page title contains 'DEBİM'.
        VERIFICATION: Page loads successfully.
        """
        assert self.lp.is_on_login_page(), "DEBİM page did not load"
        title = self.lp.get_page_title()
        assert "DEBİM" in title or "DEBIM" in title, \
            f"Page title should contain 'DEBİM', got: {title}"

    def test_username_field_exists(self):
        """
        TEST: Username field exists on the page.
        EXPECTED: 'inputName' ID element is in DOM.
        VERIFICATION: Element can be located in DOM.
        """
        assert self.lp.is_username_field_present(), \
            "Username field not found on page"

    def test_password_field_exists(self):
        """
        TEST: Password field exists on the page.
        EXPECTED: 'inputPassword' ID element is in DOM.
        VERIFICATION: Element can be located in DOM.
        """
        assert self.lp.is_password_field_present(), \
            "Password field not found on page"

    def test_login_button_exists(self):
        """
        TEST: Login button exists on the page.
        EXPECTED: 'submit' ID button is in DOM.
        VERIFICATION: Button can be located in DOM.
        """
        assert self.lp.is_login_button_present(), \
            "Login button not found on page"

    def test_invalid_login_shows_error(self):
        """
        TEST: Invalid credentials show an error.
        EXPECTED: Fake credentials trigger an error message.
        VERIFICATION: Error visible OR still on login page.
        NOTE: Negative test - intentionally tries invalid login.
        """
        self.lp.login("test_invalid_user_999", "wrong_password_999")
        time.sleep(3)
        # Either error appears, or we're still on login page
        still_on_login = self.lp.is_on_login_page() and self.lp.is_username_field_present()
        assert still_on_login or self.lp.is_error_visible(), \
            "Invalid login appears to have been accepted"
