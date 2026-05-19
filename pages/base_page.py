"""
Base Page — common methods for all Page Objects.
Provides smart waiting helpers, click, type_text, and other utilities.
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    """Base class for all Page Objects. Provides reusable methods."""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def open(self, url=None):
        """Open the given URL, or BASE_URL if defined on the subclass."""
        target = url or getattr(self, "BASE_URL", None)
        if target:
            self.driver.get(target)
        return self

    def current_url(self):
        return self.driver.current_url

    def find(self, locator):
        """Wait until element is present, then return it."""
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def find_all(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    def click(self, locator):
        """Wait until element is clickable, then click it."""
        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        ).click()
        return self

    def type_text(self, locator, text):
        """Wait for element, clear it, then type text."""
        el = self.find(locator)
        el.clear()
        el.send_keys(text)
        return self

    def get_text(self, locator):
        return self.find(locator).text

    def is_visible(self, locator, timeout=None):
        """Returns True if element becomes visible within timeout."""
        try:
            WebDriverWait(self.driver, timeout or self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
