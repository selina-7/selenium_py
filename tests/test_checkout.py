"""
Checkout Flow Tests
====================
Tests the end-to-end purchase flow.
Login -> Add Product -> Cart -> Checkout -> Complete
"""
import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.test_data import USERS, PRODUCTS, CHECKOUT_VALID, CHECKOUT_NO_FIRST


class TestCheckout:
    """Tests the complete purchase flow."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Logs in before each test."""
        lp = LoginPage(driver)
        lp.open_login_page()
        u = USERS["standard"]
        lp.login(u["username"], u["password"])
        self.pp = ProductsPage(driver)

    def test_complete_purchase_flow(self):
        """
        TEST: End-to-end purchase flow completes successfully.
        FLOW:
          1. Add product to cart
          2. Navigate to cart
          3. Proceed to checkout
          4. Fill in customer information
          5. Confirm order
          6. Order completion page is shown
        EXPECTED: 'Thank you for your order!' message appears.
        VERIFICATION: is_complete() is True and confirmation contains 'Thank you'.
        """
        self.pp.add_to_cart(PRODUCTS["backpack"])
        cart = self.pp.go_to_cart()
        assert cart.is_item_in_cart(PRODUCTS["backpack"]), "Item was not added to cart"

        checkout = cart.go_to_checkout()
        checkout.fill_info(
            CHECKOUT_VALID["first_name"],
            CHECKOUT_VALID["last_name"],
            CHECKOUT_VALID["postal_code"]
        )
        checkout.continue_to_overview()

        assert checkout.get_total() > 0, "Total amount cannot be zero"
        checkout.finish_order()
        assert checkout.is_complete(), "Did not redirect to order completion page"
        assert "Thank you" in checkout.get_confirmation(), \
            "Confirmation message should contain 'Thank you'"

    def test_checkout_requires_first_name(self):
        """
        TEST: Empty First Name field prevents proceeding.
        EXPECTED: Empty First Name displays 'First Name is required' error.
        VERIFICATION: Error message contains 'First Name is required'.
        """
        self.pp.add_to_cart(PRODUCTS["backpack"])
        cart = self.pp.go_to_cart()
        checkout = cart.go_to_checkout()
        checkout.fill_info(
            CHECKOUT_NO_FIRST["first_name"],
            CHECKOUT_NO_FIRST["last_name"],
            CHECKOUT_NO_FIRST["postal_code"]
        )
        checkout.continue_to_overview()
        assert "First Name is required" in checkout.get_error(), \
            "Correct error message not displayed for empty first name"

    def test_multiple_items_purchase(self):
        """
        TEST: Purchase flow with multiple items works.
        EXPECTED: Can start with 2 items and complete checkout.
        VERIFICATION: Reaches the order completion page.
        """
        self.pp.add_to_cart(PRODUCTS["backpack"])
        self.pp.add_to_cart(PRODUCTS["bike_light"])
        cart = self.pp.go_to_cart()
        assert cart.get_item_count() == 2, "Two items could not be added to cart"

        checkout = cart.go_to_checkout()
        checkout.fill_info(
            CHECKOUT_VALID["first_name"],
            CHECKOUT_VALID["last_name"],
            CHECKOUT_VALID["postal_code"]
        )
        checkout.continue_to_overview()
        checkout.finish_order()
        assert checkout.is_complete(), "Multi-item purchase did not complete"
