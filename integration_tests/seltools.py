import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

import urlparse
HOST=''
def set_host(a):
    global HOST
    HOST=a    
    print 'Setting the host to %s' % (HOST)
def _(path):
    return urlparse.urljoin(HOST, path)



class MyTestCase(unittest.TestCase):
    def setUp(self):
        # self.driver = webdriver.Firefox()
        self.driver = self.firefoxNoImages()

    def tearDown(self):
        self.driver.quit()


    def firefoxNoImages(self):
        # http://stackoverflow.com/questions/7157994/do-not-want-images-to-load-and-css-to-render-on-firefox-in-selenium-webdriver-te
        ## get the Firefox profile object
        firefoxProfile = FirefoxProfile()
        ## Disable CSS
        # firefoxProfile.set_preference('permissions.default.stylesheet', 2)
        ## Disable images
        firefoxProfile.set_preference('permissions.default.image', 2)
        ## Disable Flash
        # firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so',
        #                              'false')
        ## Set the modified profile while creating the browser object 
        return webdriver.Firefox(firefoxProfile)

    def save_url(self):
        self.url = self.driver.current_url
        print 'Url:', self.url

    def check_url(self, msg=""):
        self.failUnless(self.driver.current_url != self.url, msg)


    def login_into_magnate(self, username, password):
        driver = self.driver
        driver.get(_("/account/login/"))
        self.save_url()

        elt_username = self.by_id("id_username")    
        elt_username.send_keys(username)    
        elt_password = self.by_id("id_password")
        elt_password.send_keys(password)
        elt_password.submit() # will submit the form
        self.check_url("Cannot login as username='%s', incorrect password?" % (username))

        
        # After successful login, 
        # make sure there is no id_username element any more
        self.assertRaises(NoSuchElementException, lambda : driver.find_element_by_id("id_username"))
        self.save_url()


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

    def assert_on_dashboard(self):
        self.by_id("dashboard_body")

	