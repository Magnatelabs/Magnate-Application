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

        # The firefox driver for selenium has a problem
        # When we are simulating a click on an element
        # that is not in the current viewport, it is
        # not working. Even if the element is under the
        # navbar, it is still not working, even though
        # it is technically visible and enabled.
        # 
        # So scroll so the element will be right under
        # the navbar.
        navbar_height=self.by_class_name('navbar-inner').size['height']
        def scroll_and_click(elt):
            self.driver.execute_script('window.scrollTo(0,%d);' % (elt.location['y'] - navbar_height) )
            elt.click()

        # We've just created a public entry; find it in the feed!
        entry = self.by_id('entry-1')

        # Let's expand it so we can see the standard picture, the (empty) list of Q&A, etc.

        scroll_and_click ( entry )

        scroll_and_click ( self.by_link_text('Ask Question') )

        self.by_id('id_title').send_keys("Original question")
        self.by_id('editor').send_keys("I am just curious about this Magnate thing. Does it work?")
        self.by_id('id_tags').send_keys("user question curious")

        scroll_and_click ( self.by_name('ask') )

        # Assumption: the question was asked successfully, we were redirected
        self.assertIn('original-question', self.driver.current_url)

        # Make sure we still see the top of the dashboard
        self.by_class_name("user_breakdown")

        # Go back to the regular dashboard
        driver.get(_("/dash/dashboard"))
        # Make sure we are on the dashboard
        self.by_class_name("user_breakdown")
        # Once again select the first entry!
        entry = self.by_id('entry-1')
        # Select it once again; see if we can see our question on the right
        
        scroll_and_click( entry )

        # Now very important; see if we see this question we've just asked!
        # It should be shown after we've clicked once again on the entry
        link=self.by_partial_link_text('Original question')

        scroll_and_click(link)

        # try to vote for the question, up or down (whichever comes first, probably up)
        scroll_and_click( self.by_class_name('post-vote') )
        # it should say we can't vote for our own questions; click 'ok'        
        scroll_and_click( self.by_class_name('dialog-yes') )

        editor=self.by_id('editor')
        editor.send_keys("I am trying to answer my own question. Please, be kind...")
        # not a great way to locate the submit button
        # better to give it some id..
        scroll_and_click( self.by_class_name('submit') )

        # Make sure we still see the dashboard
        self.by_class_name("user_breakdown")

if __name__ == "__main__":
    unittest.main()
