# Do not run this file manually!
#
# Instead:
# cd ..
# ./selenium_tests.sh
#
# This is so the Django development server and the Selenium server could be started.

from selenium import selenium, webdriver
import unittest, time, re
import sys

print "All Selenium Tests for Magnate"
print "Expecting Django server on port 8123"

import urlparse
def _(path):
    return urlparse.urljoin('http://127.0.0.1:8123/', path)

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
    
    def tearDown(self):
  ###      self.selenium.stop()
  ###      self.assertEqual([], self.verificationErrors)
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
