import sys
import os
import requests
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import warnings

from django.contrib.auth.models import User
from core.db.manager import DataHubManager


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):  # only gets executed once
        super(FunctionalTest, cls).setUpClass()
        if os.environ.get('DATAHUB_DOCKER_TESTING') == 'true':
            # web is the name of the nginx Docker container.
            cls.server_url = 'http://web'
            return

        for arg in sys.argv:
            # look for the liveserver string when
            # initializing
            if 'liveserver' in arg:
                # skip the normal setup and use a server_url variable
                cls.server_url = 'http://' + arg.split('=')[1]
                return

        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super(FunctionalTest, cls).tearDownClass()

    def setUp(self):
        if os.environ.get('DATAHUB_DOCKER_TESTING') == 'true':
            desired_capabilities = DesiredCapabilities.PHANTOMJS
            desired_capabilities['acceptSslCerts'] = True

            self.browser = webdriver.Remote(
                # phantomjs is the name of the phantomjs Docker container.
                command_executor='http://phantomjs:8910',
                desired_capabilities=DesiredCapabilities.PHANTOMJS)
        else:
            self.browser = webdriver.PhantomJS()

        self.browser.implicitly_wait(3)

        # default username and password for loggin in a user manually
        # use only lowercase here
        self.username = 'delete_me_cdefghi'
        self.password = 'cdefghi'

    def tearDown(self):
        # Delete all users whose name starts with 'delete_me_'.
        all_users = User.objects.all()
        test_users = all_users.filter(username__startswith='delete_me_')
        for user in test_users:
            DataHubManager.remove_user(user.username, remove_db=True)
            user.delete()
        self.browser.quit()

    def delete_user(self, username):
        user = User.objects.get(username=username)
        DataHubManager.remove_user(user.username, remove_db=True)
        user.delete()

    def check_external_links(self):
        # supress warnings for testing external links
        # Particularly, because local testing will give unverified certs errors
        # print('\n\n---- TESTING EXTERNAL LINKS ----\n')
        # print('--THIS MAKE TAKE A FEW SECONDS--\n\n')

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self._check_external_links()

    def _check_external_links(self):
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
        self.browser.find_element_by_id('id_username').send_keys(self.username)

        # Justin adds an email
        self.browser.find_element_by_id('id_email').send_keys(
            self.username + '@sharklasers.com'
        )

        # Justin adds a password
        self.browser.find_element_by_id('id_password').send_keys(self.password)

        # Justin clicks sign up
        self.browser.find_element_by_id('id_sign_up_action').click()

    def sign_in_manually(self):
        # Justin goes to the sign in page
        self.browser.get(self.server_url + '/account/login')

        # He fills in his username and password
        self.browser.find_element_by_id('id_username').send_keys(self.username)
        self.browser.find_element_by_id('id_password').send_keys(self.password)

        # He clicks sign in
        self.browser.find_element_by_id('id_sign_in_action').click()

    def create_repo(self, repo_name):
        # Justin goes to the main/repos page
        self.browser.get(self.server_url + '/browse/' + self.username)

        # He clicks the add repo button
        self.browser.find_element_by_class_name('glyphicon-plus').click()

        # type the new repo id
        self.browser.find_element_by_id('new_repo_name').send_keys(repo_name)

        # click create
        self.browser.find_element_by_id('new_repo_create').click()

        # check to see that the repo name appears on the page. Click on it.
        self.browser.find_element_by_link_text(repo_name).click()

        # check to see that the url is formatted correctly
        repo_url = self.browser.current_url
        regex = '\/browse\/' + self.username + '\/' + repo_name + '\/tables'
        self.assertRegexpMatches(repo_url, regex)

    def create_table_programmatically(self, repo_name, table_name):
        # Justin goes to the main/repos page
        self.browser.get(self.server_url + '/browse/' + self.username)

        # check to see that the repo name appears on the page. Click on it.
        self.browser.find_element_by_link_text(repo_name).click()

        ddl = ('create table ' + repo_name + '.' +
               table_name + ' (id integer, words text)')

        # type some DDL into the sql field
        self.browser.find_element_by_id('txt-sql').send_keys(ddl)

        # click "run"
        self.browser.find_element_by_id('btn-run').click()

        # Go back to the repo page
        url = (self.server_url + '/browse/' + self.username + '/' + repo_name)
        self.browser.get(url)

        # check to see whether the table is there
        self.browser.find_element_by_link_text(table_name).click()

        # check to see that we're not in the table view
        table_url = self.browser.current_url
        regex = ('\/browse\/' + self.username +
                 '\/' + repo_name + '\/table\/' + table_name )

        self.assertRegexpMatches(table_url, regex)
