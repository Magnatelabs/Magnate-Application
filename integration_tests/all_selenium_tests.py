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

from seltools import MyTestCase, set_host, _
set_host('http://127.0.0.1:8123/')

print "All Selenium Tests for Magnate"
print "Expecting Django server on port 8123"


class main_page(MyTestCase):
    def test_main_page(self):
        # See http://selenium-python.readthedocs.org/en/latest/getting-started.html#using-selenium-to-write-tests
        driver = self.driver
        driver.get(_("/"))

        indexbanner=self.by_class_name("indexbanner")
        self.assertIn('Unleash your inner mogul', indexbanner.text)
    

if __name__ == "__main__":
    unittest.main()
