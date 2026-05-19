"""
Products Page Tests
====================
Tests product listing, sorting, and add-to-cart functionality.
"""
import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.test_data import USERS, PRODUCTS


class TestProducts:
    """Tests all products page functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Logs in before each test and navigates to products page."""
        lp = LoginPage(driver)
        lp.open_login_page()
        u = USERS["standard"]
        lp.login(u["username"], u["password"])
        self.pp = ProductsPage(driver)

    def test_products_page_loaded(self):
        """
        TEST: Products page loads correctly after login.
        EXPECTED: URL contains inventory.html, page title is 'Products'.
        VERIFICATION: is_on_page() returns True and title is 'Products'.
        """
        assert self.pp.is_on_page(), "Did not redirect to products page"
        assert self.pp.get_title() == "Products", "Page title is incorrect"

    def test_six_products_listed(self):
        """
        TEST: Exactly 6 products are listed on the page.
        EXPECTED: SauceDemo shows 6 products for standard user.
        VERIFICATION: Length of product names list is 6.
        """
        names = self.pp.get_product_names()
        assert len(names) == 6, f"Expected 6 products, found: {len(names)}"

    def test_add_single_item(self):
        """
        TEST: A single product can be added to cart.
        EXPECTED: After clicking 'Add to cart', cart badge shows '1'.
        VERIFICATION: Cart counter equals 1.
        """
        self.pp.add_to_cart(PRODUCTS["backpack"])
        assert self.pp.get_cart_count() == 1, "Cart counter should be 1 after adding item"

    def test_add_multiple_items(self):
        """
        TEST: Multiple products can be added to cart.
        EXPECTED: After adding 2 items, cart badge shows '2'.
        VERIFICATION: Counter updates correctly with each addition.
        """
        self.pp.add_to_cart(PRODUCTS["backpack"])
        self.pp.add_to_cart(PRODUCTS["bike_light"])
        assert self.pp.get_cart_count() == 2, "Cart counter should be 2 after adding two items"

    def test_remove_item(self):
        """
        TEST: Items added to cart can be removed.
        EXPECTED: 'Add to cart' becomes 'Remove' after adding;
                   clicking 'Remove' takes the item out of cart.
        VERIFICATION: Cart counter is 0 after removal.
        """
        self.pp.add_to_cart(PRODUCTS["backpack"])
        self.pp.remove_from_cart(PRODUCTS["backpack"])
        assert self.pp.get_cart_count() == 0, "Cart counter should be 0 after removal"

    def test_sort_a_to_z(self):
        """
        TEST: Products can be sorted alphabetically A to Z.
        EXPECTED: 'Name (A to Z)' sorts products alphabetically.
        VERIFICATION: Product names match Python's sorted() output.
        """
        self.pp.sort_by("az")
        names = self.pp.get_product_names()
        assert names == sorted(names), "Products are not sorted A to Z"

    def test_sort_z_to_a(self):
        """
        TEST: Products can be sorted Z to A in reverse alphabetical order.
        EXPECTED: 'Name (Z to A)' sorts products in reverse alphabetical order.
        VERIFICATION: Product names match sorted(reverse=True) output.
        """
        self.pp.sort_by("za")
        names = self.pp.get_product_names()
        assert names == sorted(names, reverse=True), "Products are not sorted Z to A"

    def test_sort_price_low_high(self):
        """
        TEST: Products can be sorted from low to high price.
        EXPECTED: 'Price (low to high)' sorts by ascending price.
        VERIFICATION: Price list is in ascending order.
        """
        self.pp.sort_by("lohi")
        prices = self.pp.get_product_prices()
        assert prices == sorted(prices), "Prices are not in ascending order"

    def test_sort_price_high_low(self):
        """
        TEST: Products can be sorted from high to low price.
        EXPECTED: 'Price (high to low)' sorts by descending price.
        VERIFICATION: Price list is in descending order.
        """
        self.pp.sort_by("hilo")
        prices = self.pp.get_product_prices()
        assert prices == sorted(prices, reverse=True), "Prices are not in descending order"

    def test_logout(self):
        """
        TEST: User can log out.
        EXPECTED: Clicking 'Logout' from burger menu returns to login page.
        VERIFICATION: URL no longer contains 'inventory'.
        """
        self.pp.logout()
        assert "inventory" not in self.pp.current_url(), "Logout failed"
