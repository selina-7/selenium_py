"""
Cart Page Tests
================
Tests cart verification and cart-related operations.
"""
import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.test_data import USERS, PRODUCTS


class TestCart:
    """Tests all cart page functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Logs in before each test."""
        lp = LoginPage(driver)
        lp.open_login_page()
        u = USERS["standard"]
        lp.login(u["username"], u["password"])
        self.pp = ProductsPage(driver)

    def test_cart_page_loads(self):
        """
        TEST: Cart page is accessible.
        EXPECTED: Clicking cart icon navigates to cart.html.
        VERIFICATION: URL contains 'cart.html'.
        """
        cart = self.pp.go_to_cart()
        assert cart.is_on_page(), "Did not redirect to cart page"

    def test_added_item_in_cart(self):
        """
        TEST: Added items appear correctly in cart.
        EXPECTED: After adding 'Backpack', it appears as 'Sauce Labs Backpack'.
        VERIFICATION: is_item_in_cart() returns True.
        """
        self.pp.add_to_cart(PRODUCTS["backpack"])
        cart = self.pp.go_to_cart()
        assert cart.is_item_in_cart(PRODUCTS["backpack"]), \
            "Added item not found in cart"

    def test_cart_item_count(self):
        """
        TEST: Total number of items in cart is correct.
        EXPECTED: After adding 2 items, cart shows 2 cart_item elements.
        VERIFICATION: get_item_count() returns 2.
        """
        self.pp.add_to_cart(PRODUCTS["backpack"])
        self.pp.add_to_cart(PRODUCTS["bike_light"])
        cart = self.pp.go_to_cart()
        assert cart.get_item_count() == 2, \
            f"Expected 2 items, found: {cart.get_item_count()}"

    def test_continue_shopping(self):
        """
        TEST: 'Continue Shopping' button works.
        EXPECTED: Clicking the button returns to products page.
        VERIFICATION: Redirects to inventory.html.
        """
        cart = self.pp.go_to_cart()
        products = cart.continue_shopping()
        assert products.is_on_page(), "Continue shopping button did not work"

    def test_empty_cart(self):
        """
        TEST: Empty cart state is displayed correctly.
        EXPECTED: With no items added, cart shows 0 items.
        VERIFICATION: get_item_count() returns 0.
        """
        cart = self.pp.go_to_cart()
        assert cart.get_item_count() == 0, "Empty cart expected but items found"
