# Testing Live Production server!

from selenium.webdriver.support.ui import Select


import unittest, time, re
import sys

from seltools import MyTestCase, set_host, _
set_host('http://magnate-%s.herokuapp.com/' % (sys.argv[1])) # 'magnate-prod' or 'magnate-staging'
# delete extra command-line options, or python's unittest will freak out
del sys.argv[1:] # http://stackoverflow.com/questions/1029891/python-unittest-is-there-a-way-to-pass-command-line-options-to-the-app

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


    def test_dashboard(self):
        driver = self.driver
        
        self.login_into_magnate(TEST_USERNAME, TEST_PASSWORD)        
        driver.get(_("/dash/dashboard"))

        # Make sure we are on the dashboard
        self.assert_on_dashboard()

    def test_contribution(self):
        real_credit_card='4111111111111111'
        broken_credit_card='123192038'
        exp_date='12/30' # increase this number after 2030
        card_code='123'  # three digits on the back

        driver = self.driver

        self.login_into_magnate(TEST_USERNAME, TEST_PASSWORD)
        driver.get(_("/contributions/home"))
        elt_link = self.by_partial_link_text("Add to the fund")
        elt_link.click()
        self.check_url()

#       The above link navigates directly to the donation_add page now
#        self.save_url()
#        elt_link = self.by_partial_link_text("Add to the fund")
#        elt_link.click()
#        self.check_url()

        
        for ind in range(3): 
            # deliberately fail the first two times
            to_succeed = (ind==2)

            self.save_url()
            if not to_succeed:
                # pick the first amount, probably $10.00
                elt_radio = self.by_class_name("radio")
                elt_radio.click()
                elt_radio.submit()
            else:
                # let's enter some ridiculous amount to be rounded to $0.01 (one cent)

                da_elt = self.by_id("id_donation_amount")
                # Use Backspace to clear the donation amount box
                for i in range(len('0.00')):
                    da_elt.send_keys(u'\u0008')
                    
                da_elt.send_keys("0.0123456789")
                # change focus, so the donation amount can be fixed by Javascript code
                self.driver.find_element_by_css_selector('body').send_keys(" ")
                self.assertEqual(da_elt.get_attribute('value'), '0.01')
                # now submit the form
                self.by_class_name("radio").submit()


            self.check_url()
            self.assertFalse('34567' in self.driver.page_source, "It should not allow us to enter such ridiculous amounts. 0.0123456789 should have been rounded to something sensible")

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

# This is now the same URL; do not check.
#            self.check_url()

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

            self.by_id("id_x_card_num").send_keys([broken_credit_card, real_credit_card][to_succeed])
            self.by_id("id_x_exp_date").send_keys(exp_date)
            self.by_id("id_x_card_code").send_keys(card_code)
            # First name is already entered
            ###driver.find_element_by_id("id_x_first_name").send_keys("Test")
            # Last name is already entered
            ###driver.find_element_by_id("id_x_last_name").send_keys("Selenium")
            # Zip code is already entered
            ###driver.find_element_by_id("id_x_zip").send_keys("10118")

            import seltools
            # Exactly one must be true
            self.assertTrue(bool('staging' in seltools.HOST) != bool('prod' in seltools.HOST))
            if 'staging' in seltools.HOST:
                self.assertIn('test.authorize.net', self.driver.page_source)
                self.assertNotIn('secure.authorize.net', self.driver.page_source)
            else:
                self.assertIn('secure.authorize.net', self.driver.page_source)
                self.assertNotIn('test.authorize.net', self.driver.page_source)

            # Checkbox "I accept the terms and conditions...""
            checkbox = self.by_name("01")
            checkbox.click()
            checkbox.submit()

            if to_succeed:                
                ## Do not rely on page_source, may take time to load
                ## self.assertNotIn("The credit card number is invalid", driver.page_source)
                self.assertNotIn("The+credit+card+number+is+invalid", self.driver.current_url)
                self.assertIn('success', self.driver.current_url)
                # Neither perfect nor necessary, but I want to triple-check that the donation went through
                self.assertEqual(self.by_class_name('light').text, 'You are now ready to participate in the MagnateFund!')
            else:
                ## Do not rely on page_source, may take time to load
                ## self.assertIn("The credit card number is invalid", driver.page_source)
                self.assertIn("The+credit+card+number+is+invalid", self.driver.current_url)



if __name__ == "__main__":
    unittest.main()
