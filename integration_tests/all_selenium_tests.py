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


from selenium.webdriver.support.ui import Select

from seltools import MyTestCase, set_host, _
set_host('http://127.0.0.1:8123/')

# We expect the site owner (root, root) to be pre-created before integration testing.
ROOT_LOGIN='root'
ROOT_PASSWORD='root'

print "All Selenium Tests for Magnate"
print "Expecting Django server on port 8123"


class main_page(MyTestCase):
    def test_main_page(self):
        # See http://selenium-python.readthedocs.org/en/latest/getting-started.html#using-selenium-to-write-tests
        driver = self.driver
        driver.get(_("/"))

        indexbanner=self.by_class_name("indexbanner")
        self.assertIn('Unleash your inner mogul', indexbanner.text)

    def test_dashboard(self):
        driver = self.driver

        self.login_into_magnate(ROOT_LOGIN, ROOT_PASSWORD)
        driver.get(_("/admin/zinnia/entry/"))
        self.by_class_name("addlink").click()

        self.by_id("id_title").send_keys("Magnate opens tomorrow. Let's celebrate!")
        
        select = Select(self.by_id("id_status"))
        select.select_by_visible_text("published")

        self.driver.switch_to.frame("")
        self.by_class_name("wym_iframe").send_keys("Welcome to the website. This is just some sample content... \n\n\nSed ut perspiciatis, unde omnis iste natus error sit voluptatem ")
        
        self.driver.switch_to.parent_frame()
        self.by_name("_save").click()

        driver.get(_("/dash/dashboard"))

        # Make sure we are on the dashboard
        self.by_class_name("user_breakdown")

        # We've just created a public entry; find it in the feed!
        entry = self.by_id('entry-1')

        # Let's expand it so we can see the standard picture, the (empty) list of Q&A, etc.

        entry.click()
        self.by_link_text('Ask Question').click()

        self.by_id('id_title').send_keys("First question")
        self.by_id('editor').send_keys("I am just curious about this Magnate thing. Does it work?")
        self.by_id('id_tags').send_keys("user question curious")
        self.by_name('ask').click()

        # Assumption: the question was asked successfully, we were redirected
        self.assertIn('first-question', self.driver.current_url)

        # Make sure we still see the top of the dashboard
        self.by_class_name("user_breakdown")


if __name__ == "__main__":
    unittest.main()
