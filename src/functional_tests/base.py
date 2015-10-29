import sys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


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
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
