"""
Login Page Tests
=================
Tests all scenarios on the SauceDemo login page.
Includes both positive (successful login) and negative (failed login) cases.
"""
import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.test_data import USERS, VALID_USERS, INVALID_USERS


class TestLogin:
    """Tests login scenarios."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Opens the login page before each test."""
        self.lp = LoginPage(driver)
        self.lp.open_login_page()

    def test_successful_login(self):
        """
        TEST: Successful login with standard user.
        EXPECTED: Valid credentials redirect to products page.
        VERIFICATION: URL contains 'inventory.html' and page title is 'Products'.
        """
        u = USERS["standard"]
        self.lp.login(u["username"], u["password"])
        pp = ProductsPage(self.lp.driver)
        assert pp.is_on_page(), "Did not redirect to products page after login"
        assert pp.get_title() == "Products", "Page title should be 'Products'"

    @pytest.mark.parametrize("username,password", VALID_USERS)
    def test_valid_users_can_login(self, username, password):
        """
        TEST: All valid user types can log in (parametrized).
        EXPECTED: standard_user, performance_glitch_user reach products page.
        VERIFICATION: Each user redirects to inventory.html.
        """
        self.lp.login(username, password)
        pp = ProductsPage(self.lp.driver)
        assert pp.is_on_page(), f"Login failed for user: {username}"

    @pytest.mark.parametrize("username,password,expected_error", INVALID_USERS)
    def test_invalid_login_shows_error(self, username, password, expected_error):
        """
        TEST: Invalid credentials display an error message (parametrized).
        SCENARIOS: Wrong username, wrong password, empty username, empty password.
        EXPECTED: An appropriate error message is shown each time.
        VERIFICATION: Error message is visible and contains expected text.
        """
        self.lp.login(username, password)
        assert self.lp.is_error_visible(), "Error message did not appear"
        assert expected_error in self.lp.get_error(), \
            f"Expected: '{expected_error}', Got: '{self.lp.get_error()}'"

    def test_locked_user_cannot_login(self):
        """
        TEST: Locked user (locked_out_user) cannot log in.
        EXPECTED: Login is blocked because the account is locked.
        VERIFICATION: Error message containing 'locked out' is displayed.
        """
        u = USERS["locked"]
        self.lp.login(u["username"], u["password"])
        assert self.lp.is_error_visible(), "Error message not shown for locked user"
        assert "locked out" in self.lp.get_error(), \
            "Error message should contain 'locked out'"

    def test_error_can_be_closed(self):
        """
        TEST: Error message can be closed via X button.
        EXPECTED: Clicking X after an error hides the message.
        VERIFICATION: Error is no longer visible after closing.
        """
        self.lp.login("wrong", "wrong")
        assert self.lp.is_error_visible(), "Error message should be visible first"
        self.lp.close_error()
        assert not self.lp.is_error_visible(), "Error message could not be closed"
