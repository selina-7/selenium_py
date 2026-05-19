"""
SauceDemo Checkout Page — Page Object.
Handles the multi-step checkout flow.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Page Object for SauceDemo checkout flow."""

    FIRST_NAME   = (By.ID, "first-name")
    LAST_NAME    = (By.ID, "last-name")
    POSTAL_CODE  = (By.ID, "postal-code")
    BTN_CONTINUE = (By.ID, "continue")
    BTN_FINISH   = (By.ID, "finish")
    ERROR_MSG    = (By.CSS_SELECTOR, "h3[data-test='error']")
    TOTAL_LABEL  = (By.CLASS_NAME, "summary_total_label")
    CONFIRMATION = (By.CLASS_NAME, "complete-header")

    def fill_info(self, first_name, last_name, postal_code):
        """Fill the customer information form."""
        self.type_text(self.FIRST_NAME, first_name)
        self.type_text(self.LAST_NAME, last_name)
        self.type_text(self.POSTAL_CODE, postal_code)
        return self

    def continue_to_overview(self):
        self.click(self.BTN_CONTINUE)
        return self

    def finish_order(self):
        self.click(self.BTN_FINISH)
        return self

    def get_error(self):
        if self.is_visible(self.ERROR_MSG, timeout=5):
            return self.get_text(self.ERROR_MSG)
        return ""

    def get_total(self):
        """Returns numeric total from the summary."""
        text = self.get_text(self.TOTAL_LABEL)
        # Example text: "Total: $32.39"
        return float(text.split("$")[1])

    def is_complete(self):
        return "checkout-complete.html" in self.current_url()

    def get_confirmation(self):
        return self.get_text(self.CONFIRMATION)
