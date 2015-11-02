import sys
import requests
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import warnings


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):  # only gets executed once
        for arg in sys.argv:
            # look for the liveserver string when
            # initializing
            if 'liveserver' in arg:
                # skip the normal setup and use a server_url variable
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super(FunctionalTest, cls).setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super(FunctionalTest, cls).tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

        # default username and password for loggin in a user manually
        # use only lowercase here
        self.username = 'cdefghi'
        self.password = 'cdefghi'

    def tearDown(self):
        self.browser.quit()

    def test_external_links(self):
        # supress warnings for testing external links
        # Particularly, because local testing will give unverified certs errors
        # print('\n\n---- TESTING EXTERNAL LINKS ----\n')
        # print('--THIS MAKE TAKE A FEW SECONDS--\n\n')

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self._test_external_links()

    def _test_external_links(self):
        # Justin gets a list of external links
        links = self.browser.find_elements_by_xpath(
            "//a[(starts-with(@href, 'http'))]")
        links = map(lambda x: x.get_attribute('href'), links)

        # he prepares to make note of which tests fail
        failing_links = []

        # He tries each of them, to make sure that they work
        for link in links:
            try:
                r = requests.get(link, verify=False)
                if r.status_code != (200 or 302):
                    failing_link = {'link': link, 'reason': r.status_code}
                    failing_links.append(failing_link)
            except:
                failing_link = {'link': link, 'reason': 'exception'}
                failing_links.append(failing_link)

        # If there are links that failed, the test fails
        if len(failing_links) > 0:
            print("Some links on the did not check out")
            self.fail(failing_links)

    def sign_up_manually(self):
        self.browser.get(self.server_url + '/account/register')

        # Justin adds a username
        self.browser.find_element_by_id('username').send_keys(self.username)

        # Justin adds an email
        self.browser.find_element_by_id('email').send_keys(
            self.username+'@sharklasers.com'
        )

        # Justin adds a password
        self.browser.find_element_by_id('password').send_keys(self.password)

        # Justin clicks sign up
        self.browser.find_element_by_id('id_register').click()


    def sign_in_manually(self):
        # Justin goes to the sign in page
        self.browser.get(self.server_url + '/account/login')

        # He fills in his username and password
        self.browser.find_element_by_id('id_username').send_keys(self.username)
        self.browser.find_element_by_id('id_password').send_keys(self.password)

        # He clicks sign in 
        self.browser.find_element_by_id('id_sign_in_action').click()