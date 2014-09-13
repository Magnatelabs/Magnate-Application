# Testing Live Production server!

from selenium.webdriver.support.ui import Select


import unittest, time, re
import sys

from seltools import MyTestCase, set_host, _
set_host('http://magnate-prod.herokuapp.com/')

print "Testing Live Production"

# Get TEST_USERNAME and TEST_PASSWORD from the file test_credentials.pysh
import os
dirname, filename = os.path.split(os.path.abspath(__file__))

import imp
credentials=imp.load_source('test_credentials', os.path.join(dirname, 'test_credentials.pysh'))
TEST_USERNAME=credentials.TEST_USERNAME
TEST_PASSWORD=credentials.TEST_PASSWORD




class main_page(MyTestCase):


    def test_main_page(self):
        # See http://selenium-python.readthedocs.org/en/latest/getting-started.html#using-selenium-to-write-tests
        driver = self.driver
        driver.get(_("/"))

        indexbanner=self.by_class_name("indexbanner")
        self.assertIn('Unleash your inner mogul', indexbanner.text)

    

    def test_login(self):
        driver = self.driver

        self.login_into_magnate(TEST_USERNAME, TEST_PASSWORD)
        driver.get(_("/fund/home"))
        elt_link = self.by_partial_link_text("Add to the fund")
        elt_link.click()
        self.check_url()

#       The above link navigates directly to the donation_add page now
#        self.save_url()
#        elt_link = self.by_partial_link_text("Add to the fund")
#        elt_link.click()
#        self.check_url()

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

# This does not work any more:
# (This is for ordinary select boxes).
#            select = Select(driver.find_element_by_name("Card-type"))
#            select.select_by_visible_text("Visa")

# Now we are using a fancy select box.
# First click to open the drop down.
# There is only one sbHolder on this page.
###            self.by_class_name('sbHolder').click()
# Now pick Visa.
###            self.by_partial_link_text('Visa').click()

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



if __name__ == "__main__":
    unittest.main()
