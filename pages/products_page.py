"""
SauceDemo Products Page — Page Object.
Handles product listing, sorting, and cart operations.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


# Hard-coded button IDs (SauceDemo IDs cannot be reliably generated from slugs)
PRODUCT_BUTTON_IDS = {
    "Sauce Labs Backpack":               "add-to-cart-sauce-labs-backpack",
    "Sauce Labs Bike Light":             "add-to-cart-sauce-labs-bike-light",
    "Sauce Labs Bolt T-Shirt":           "add-to-cart-sauce-labs-bolt-t-shirt",
    "Sauce Labs Fleece Jacket":          "add-to-cart-sauce-labs-fleece-jacket",
    "Sauce Labs Onesie":                 "add-to-cart-sauce-labs-onesie",
    "Test.allTheThings() T-Shirt (Red)": "add-to-cart-test.allthethings()-t-shirt-(red)",
}

REMOVE_BUTTON_IDS = {
    "Sauce Labs Backpack":               "remove-sauce-labs-backpack",
    "Sauce Labs Bike Light":             "remove-sauce-labs-bike-light",
    "Sauce Labs Bolt T-Shirt":           "remove-sauce-labs-bolt-t-shirt",
    "Sauce Labs Fleece Jacket":          "remove-sauce-labs-fleece-jacket",
    "Sauce Labs Onesie":                 "remove-sauce-labs-onesie",
    "Test.allTheThings() T-Shirt (Red)": "remove-test.allthethings()-t-shirt-(red)",
}


class ProductsPage(BasePage):
    """Page Object for SauceDemo products page."""

    TITLE          = (By.CLASS_NAME, "title")
    PRODUCT_NAMES  = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    SORT_SELECT    = (By.CLASS_NAME, "product_sort_container")
    CART_ICON      = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE     = (By.CLASS_NAME, "shopping_cart_badge")
    BURGER_MENU    = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK    = (By.ID, "logout_sidebar_link")

    def is_on_page(self):
        return "inventory.html" in self.current_url()

    def get_title(self):
        return self.get_text(self.TITLE)

    def get_product_names(self):
        return [el.text for el in self.find_all(self.PRODUCT_NAMES)]

    def get_product_prices(self):
        return [float(el.text.replace("$", "")) for el in self.find_all(self.PRODUCT_PRICES)]

    def add_to_cart(self, product_name):
        button_id = PRODUCT_BUTTON_IDS.get(product_name)
        if not button_id:
            raise ValueError(f"Unknown product: {product_name}")
        # Click the button
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, button_id))
        )
        btn.click()
        # Wait until "Remove" button appears - confirms click was registered
        remove_id = button_id.replace("add-to-cart-", "remove-")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, remove_id))
        )
        return self

    def remove_from_cart(self, product_name):
        button_id = REMOVE_BUTTON_IDS.get(product_name)
        if not button_id:
            raise ValueError(f"Unknown product: {product_name}")
        self.click((By.ID, button_id))
        return self

    def get_cart_count(self):
        if self.is_visible(self.CART_BADGE, timeout=5):
            return int(self.get_text(self.CART_BADGE))
        return 0

    def go_to_cart(self):
        self.click(self.CART_ICON)
        from pages.cart_page import CartPage
        return CartPage(self.driver)

    def sort_by(self, value):
        Select(self.find(self.SORT_SELECT)).select_by_value(value)
        return self

    def logout(self):
        self.click(self.BURGER_MENU)
        self.click(self.LOGOUT_LINK)
