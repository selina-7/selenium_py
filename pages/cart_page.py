"""
SauceDemo Cart Page — Page Object.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    """Page Object for SauceDemo cart page."""

    TITLE           = (By.CLASS_NAME, "title")
    CART_ITEMS      = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES      = (By.CLASS_NAME, "inventory_item_name")
    BTN_CHECKOUT    = (By.ID, "checkout")
    BTN_CONTINUE    = (By.ID, "continue-shopping")

    def is_on_page(self):
        return "cart.html" in self.current_url()

    def get_item_count(self):
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def is_item_in_cart(self, product_name):
        items = self.driver.find_elements(*self.ITEM_NAMES)
        return any(it.text == product_name for it in items)

    def go_to_checkout(self):
        self.click(self.BTN_CHECKOUT)
        from pages.checkout_page import CheckoutPage
        return CheckoutPage(self.driver)

    def continue_shopping(self):
        self.click(self.BTN_CONTINUE)
        from pages.products_page import ProductsPage
        return ProductsPage(self.driver)
