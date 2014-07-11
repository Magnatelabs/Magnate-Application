# Testing Live Production server!

from selenium import selenium, webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
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

    def test_main_page(self):
#        sel = self.selenium
#        sel.open("/wefewwef/")
#        sel.open("/account/login/")


        # See http://selenium-python.readthedocs.org/en/latest/getting-started.html#using-selenium-to-write-tests
        driver = self.driver
        driver.get(_("/"))
        self.assertIn('Unleash your inner mogul', driver.page_source)
        
#        sel.click("nav_tags")
#        sel.wait_for_page_to_load("30000")
#        try: self.failUnless(sel.is_text_present("Tag list"))
#        except AssertionError, e: self.verificationErrors.append(str(e))
#        try: self.failUnless(sel.is_text_present("by name"))
#        except AssertionError, e: self.verificationErrors.append(str(e))
#        try: self.failUnless(sel.is_text_present("by popularity"))
#        except AssertionError, e: self.verificationErrors.append(str(e))
    
    def save_url(self):
        self.url = self.driver.current_url
        print 'Url:', self.url

    def check_url(self, msg=""):
        self.failUnless(self.driver.current_url != self.url, msg)


    def test_login(self):
        driver = self.driver
        driver.get(_("/account/login/"))
        self.save_url()
        elt_username = driver.find_element_by_id("id_username")    
        elt_username.send_keys(TEST_USERNAME)    
        elt_password = driver.find_element_by_id("id_password")
        elt_password.send_keys(TEST_PASSWORD)
        elt_password.submit() # will submit the form
        self.check_url("Cannot login as username='%s', incorrect password?" % (TEST_USERNAME))

        
        # After successful login, 
        # make sure there is no id_username element any more
        def foo():
            driver.find_element_by_id("id_username")
        self.assertRaises(NoSuchElementException, foo)

        self.save_url()
        elt_link = driver.find_element_by_partial_link_text("Add more to the fund")
        elt_link.click()
        self.check_url()

        self.save_url()
        elt_link = driver.find_element_by_partial_link_text("Add to the fund")
        elt_link.click()
        self.check_url()

        # Try the same thing several times
        for ind in range(3): 

            # pick the first amount, probably $10.00
            self.save_url()
            elt_radio = driver.find_element_by_class_name("radio")
            elt_radio.click()
            elt_radio.submit()
            self.check_url()

            # Enter some billing address. Use China as the country.
            self.save_url()
            self.assertIn("Enter billing address", driver.page_source)
            driver.find_element_by_id("id_first_name").send_keys("Test")
            driver.find_element_by_id("id_last_name").send_keys("Selenium")
            driver.find_element_by_id("id_address").send_keys("350 5th Ave")
            driver.find_element_by_id("id_city").send_keys("New York")
            driver.find_element_by_id("id_zipcode").send_keys("10118")

            select = Select(driver.find_element_by_id("id_country"))
            select.select_by_visible_text("China")
            driver.find_element_by_id("id_country").submit()
            self.check_url()

            self.save_url()
            self.assertIn("Check your order and pay", driver.page_source)
            select = Select(driver.find_element_by_name("Card-type"))
            select.select_by_visible_text("Visa")
            driver.find_element_by_id("id_x_card_num").send_keys("123192038")
            driver.find_element_by_id("id_x_exp_date").send_keys("01/05")
            driver.find_element_by_id("id_x_card_code").send_keys("123")
            # First name is already entered
            ###driver.find_element_by_id("id_x_first_name").send_keys("Test")
            # Last name is already entered
            ###driver.find_element_by_id("id_x_last_name").send_keys("Selenium")
            # Zip code is already entered
            ###driver.find_element_by_id("id_x_zip").send_keys("10118")
            
            # Checkbox "I accept the terms and conditions...""
            checkbox = driver.find_element_by_name("01")
            checkbox.click()
            checkbox.submit()

            self.assertIn("The credit card number is invalid", driver.page_source)


    def tearDown(self):
  ###      self.selenium.stop()
  ###      self.assertEqual([], self.verificationErrors)
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
