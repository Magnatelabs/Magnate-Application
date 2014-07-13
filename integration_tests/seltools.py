import unittest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui


class MyTestCase(unittest.TestCase):
    # assert that the element is visible within 10 seconds
    def assertVisible(self, by, locator, timeout=10):
        try:
            ui.WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, locator)))
        except TimeoutException:
            self.assertTrue(False, "Element with %s='%s' not found after %d seconds" % (str(by), locator, timeout))

    # Helper functions
    # Try to find an element and wait if it is not found
    # (This may happen if the page hasn't fully loaded yet.)
    # We do not want an implicit wait as sometimes we expect
    # elements to be absent.


    def by_class_name(self, a):
        self.assertVisible(By.CLASS_NAME, a)
        return self.driver.find_element_by_class_name(a)

    def by_css_selector(self, a):
        self.assertVisible(By.CSS_SELECTOR, a)
        return self.driver.find_element_by_css_selector(a)

    def by_id(self, a):
        self.assertVisible(By.ID, a)
        return self.driver.find_element_by_id(a)

    def by_link_text(self, a):
        self.assertVisible(By.LINK_TEXT, a)
        return self.driver.find_element_by_link_text(a)

    def by_name(self, a):
        self.assertVisible(By.NAME, a)
        return self.driver.find_element_by_name(a)

    def by_partial_link_text(self, a):
        self.assertVisible(By.PARTIAL_LINK_TEXT, a)
        return self.driver.find_element_by_partial_link_text(a)

    def by_tag_name(self, a):
        self.assertVisible(By.TAG_NAME, a)
        return self.driver.find_element_by_tag_name(a)

    def by_xpath(self, a):
        self.assertVisible(By.XPATH, a)
        return self.driver.find_element_by_xpath(a)

	