# Testing Live Production server!

from selenium import selenium, webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui

import unittest, time, re
import sys

print "Testing Live Production"

# Get TEST_USERNAME and TEST_PASSWORD from the file test_credentials.pysh
import os
dirname, filename = os.path.split(os.path.abspath(__file__))

import imp
credentials=imp.load_source('test_credentials', os.path.join(dirname, 'test_credentials.pysh'))
TEST_USERNAME=credentials.TEST_USERNAME
TEST_PASSWORD=credentials.TEST_PASSWORD


import urlparse
def _(path):
    return urlparse.urljoin('http://magnate-prod.herokuapp.com/', path)


class main_page(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        
###        self.selenium = selenium("localhost", 4444, "*chrome", "http://127.0.0.1:8123/")
###        self.selenium.start()
   
        #self.selenium.set_timeout(1000) # do not do it; default 30000=30sec is OK

        self.driver = webdriver.Firefox()

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



    def test_main_page(self):
#        sel = self.selenium
#        sel.open("/wefewwef/")
#        sel.open("/account/login/")


        # See http://selenium-python.readthedocs.org/en/latest/getting-started.html#using-selenium-to-write-tests
        driver = self.driver
        driver.get(_("/"))

        indexbanner=self.by_class_name("indexbanner")
        self.assertIn('Unleash your inner mogul', indexbanner.text)

    
    def save_url(self):
        self.url = self.driver.current_url
        print 'Url:', self.url

    def check_url(self, msg=""):
        self.failUnless(self.driver.current_url != self.url, msg)


    def test_login(self):
        driver = self.driver
        driver.get(_("/account/login/"))
        self.save_url()

        elt_username = self.by_id("id_username")    
        elt_username.send_keys(TEST_USERNAME)    
        elt_password = self.by_id("id_password")
        elt_password.send_keys(TEST_PASSWORD)
        elt_password.submit() # will submit the form
        self.check_url("Cannot login as username='%s', incorrect password?" % (TEST_USERNAME))

        
        # After successful login, 
        # make sure there is no id_username element any more
        def foo():
            driver.find_element_by_id("id_username")
        self.assertRaises(NoSuchElementException, foo)

        self.save_url()
        elt_link = self.by_partial_link_text("Add more to the fund")
        elt_link.click()
        self.check_url()

        self.save_url()
        elt_link = self.by_partial_link_text("Add to the fund")
        elt_link.click()
        self.check_url()

        # Try the same thing several times
        for ind in range(3): 

            # pick the first amount, probably $10.00
            self.save_url()
            elt_radio = self.by_class_name("radio")
            elt_radio.click()
            elt_radio.submit()
            self.check_url()

            # Enter some billing address. Use China as the country.
            self.save_url()

            heading=self.by_class_name('heading-inner')
            self.assertIn("Enter billing address", heading.text)
            
            self.by_id("id_first_name").send_keys("Test")
            self.by_id("id_last_name").send_keys("Selenium")
            self.by_id("id_address").send_keys("350 5th Ave")
            self.by_id("id_city").send_keys("New York")
            self.by_id("id_zipcode").send_keys("10118")

            select = Select(self.by_id("id_country"))
            select.select_by_visible_text("China")
            self.by_id("id_country").submit()
            self.check_url()

            self.save_url()

            heading=self.by_class_name('heading-inner')
            self.assertIn("Check your order and pay", heading.text)

            select = Select(driver.find_element_by_name("Card-type"))
            select.select_by_visible_text("Visa")
            self.by_id("id_x_card_num").send_keys("123192038")
            self.by_id("id_x_exp_date").send_keys("01/05")
            self.by_id("id_x_card_code").send_keys("123")
            # First name is already entered
            ###driver.find_element_by_id("id_x_first_name").send_keys("Test")
            # Last name is already entered
            ###driver.find_element_by_id("id_x_last_name").send_keys("Selenium")
            # Zip code is already entered
            ###driver.find_element_by_id("id_x_zip").send_keys("10118")
            
            # Checkbox "I accept the terms and conditions...""
            checkbox = self.by_name("01")
            checkbox.click()
            checkbox.submit()

            ## Do not rely on page_source, may take time to load
            ## self.assertIn("The credit card number is invalid", driver.page_source)
            self.assertIn("The+credit+card+number+is+invalid", self.driver.current_url)


    def tearDown(self):
  ###      self.selenium.stop()
  ###      self.assertEqual([], self.verificationErrors)
        
        #self.driver.close()
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
