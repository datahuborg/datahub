import sys
import os
import re
import datetime
import requests
import warnings

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

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
            self.browser = webdriver.Remote(
                # phantomjs is the name of the phantomjs Docker container.
                command_executor='http://phantomjs:8910',
                desired_capabilities=DesiredCapabilities.PHANTOMJS)
        else:
            self.browser = webdriver.PhantomJS()

        self.browser.set_window_size(900, 600)
        self.browser.implicitly_wait(3)

        # test users DB's/ postgres usernames/django usernames can sometimes
        # persist if previous testing didn't finish correctly.
        self.delete_all_test_users()

        # default username and password for loggin in a user manually
        # use only lowercase here
        self.username = 'delete_me_cdefghi'
        self.password = 'cdefghi'

    def tearDown(self):
        # create a screenshots directory, if necessary
        if not os.path.isdir('functional_tests/screenshots'):
            os.mkdir('functional_tests/screenshots')

        # save a screenshot of the browser
        self.browser.get_screenshot_as_file(
            'functional_tests/screenshots/' +
            str(datetime.datetime.now()) + '.png'
            )

        # delete those users
        self.delete_all_test_users()
        self.browser.quit()

    def delete_all_test_users(self):

        # When building tests, it's possible to delete some combination of the
        # django user/postgres user/postgres user database
        # This tries to catch the edge cases.
        all_users = DataHubManager.list_all_users()
        test_users = filter(lambda x: x.startswith('delete_me_'), all_users)
        for user in test_users:
            try:
                DataHubManager.remove_user(user, remove_db=True,
                                           ignore_missing_user=True)
            except:
                print('UNABLE TO DELETE USER ' + user)

        # Delete all django users whose name starts with 'delete_me_'.
        all_users = User.objects.all()
        test_users = all_users.filter(username__startswith='delete_me_')
        for user in test_users:
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

    def sign_up_manually(self, username=None, password=None):
        # check for usernames that don't start with delete_me
        if username is None:
            username = self.username
        if password is None:
            password = self.password

        self.browser.get(self.server_url + '/account/register')

        # Justin adds a username
        self.browser.find_element_by_id('id_username').send_keys(username)

        # Justin adds an email
        self.browser.find_element_by_id('id_email').send_keys(
            username + '@sharklasers.com'
        )

        # Justin adds a password
        self.browser.find_element_by_id('id_password').send_keys(password)

        # Justin clicks sign up
        self.browser.find_element_by_id('id_sign_up_action').click()

    def sign_in_manually(self, username=None, password=None):
        if username is None:
            username = self.username
        if password is None:
            password = self.password

        if not username.startswith('delete_me_'):
            self.fail('test usernames must begin with "delete_me_"')

        # Justin goes to the sign in page
        self.browser.get(self.server_url + '/account/login')

        # He fills in his username and password
        self.browser.find_element_by_id('id_username').send_keys(username)
        self.browser.find_element_by_id('id_password').send_keys(password)

        # He clicks sign in
        self.browser.find_element_by_id('id_sign_in_action').click()

    def sign_out_manually(self):
        # This requires the browser not to be in mobile mode.
        # it'd be nice to make the code less brittle, but I'm hesitant to do
        # that unless we know that there are no big UX changes coming.
        # ARC 2015-12-16
        self.browser.find_element_by_id('id_user_menu').click()
        self.browser.find_element_by_id('id_sign_out').click()

    def create_repo(self, repo_name, username=None):
        repo_name = repo_name.lower()
        if username is None:
            username = self.username

        # print('creating repo: %s for username: %s' % (repo_name, username))

        # Justin goes to the main/repos page
        self.browser.get(self.server_url + '/browse/' + username)

        # He clicks the add repo button
        self.browser.find_element_by_xpath(
            '(//a[@title="Create a New Repository"])[1]').click()

        # type the new repo id
        self.browser.find_element_by_id('new_repo_name').send_keys(repo_name)

        # click create
        self.browser.find_element_by_id('new_repo_create').click()

        # check to see that the repo name appears on the page. Click on it.
        self.browser.find_element_by_link_text(repo_name).click()

        # check to see that the url is formatted correctly
        repo_url = self.browser.current_url
        regex = r'/browse/{username}/{repo}/tables'.format(
                username=username, repo=repo_name)

        self.assertRegexpMatches(repo_url, regex)

    def delete_repo(self, repo_name, username=None):
        if username is None:
            username = self.username

        # Justin goes to the main/repos page
        self.browser.get(self.server_url + '/browse/' + username)

        # Justin clicks the delete button next to the given repo name
        xpath = ('(//table/tbody/tr[td/a/text()="{repo}"]/td/'
                 'span[@title="Delete"]/a)[1]').format(repo=repo_name)
        self.browser.find_element_by_xpath(xpath).click()

        # he confirms the delete
        xpath = '(//button[text()="Delete"])[1]'
        self.browser.find_element_by_xpath(xpath).click()

        # the repo name now does not appear on the page
        src = self.browser.page_source
        text_found = re.search(repo_name, src)

        self.assertEqual(text_found, None)

    def create_table(self, repo_name, table_name, username=None):
        repo_name = repo_name.lower()
        table_name = table_name.lower()
        if username is None:
            username = self.username

        # Justin goes to the main/repos page
        self.browser.get(self.server_url + '/browse/' + username)

        # check to see that the repo name appears on the page. Click on it.
        self.browser.find_element_by_link_text(repo_name).click()

        ddl = ('create table {repo}.{table} (id integer, words text)'
               .format(repo=repo_name, table=table_name))

        # type some DDL into the sql field
        self.browser.find_element_by_id('txt-sql').send_keys(ddl)

        # click "run"
        self.browser.find_element_by_id('btn-run').click()

        # Go back to the repo page
        url = (self.server_url + '/browse/' + username + '/' + repo_name)
        self.browser.get(url)

        # check to see whether the table is there
        self.browser.find_element_by_link_text(table_name).click()

        # check to see that we're not in the table view
        table_url = self.browser.current_url
        regex = r'/browse/{username}/{repo}/table/{table}'.format(
                username=username, repo=repo_name, table=table_name)

        self.assertRegexpMatches(table_url, regex)

    def create_view(self, repo_name, table_name, view_name, username=None):
        if username is None:
            username = self.username

        self.browser.get(self.server_url + '/browse/' + username)

        # check to see that the repo name appears on the page. Click on it.
        self.browser.find_element_by_link_text(repo_name).click()

        ddl = ('create view {repo}.{view} as select * from {repo}.{table}'
               .format(repo=repo_name, view=view_name, table=table_name))

        # type some DDL into the sql field
        self.browser.find_element_by_id('txt-sql').send_keys(ddl)

        # click "run"
        self.browser.find_element_by_id('btn-run').click()

        # Go back to the repo page
        url = (self.server_url + '/browse/' + username + '/' + repo_name)
        self.browser.get(url)

        # check to see whether the table is there
        self.browser.find_element_by_link_text(view_name).click()

        # check to see that we're not in the table view
        table_url = self.browser.current_url
        regex = r'/browse/{username}/{repo}/table/{view}'.format(
                username=username, repo=repo_name, view=view_name)

        self.assertRegexpMatches(table_url, regex)

    def make_repo_public(self, repo):
        self.browser.find_element_by_id('logo').click()

        # click the collaborators button next to the repo
        xpath = ('(//table/tbody/tr[td/a/text()="{repo}"]/td/a[text()['
                 'contains(.,"collaborator(s)")]])[1]').format(repo=repo)
        self.browser.find_element_by_xpath(xpath).click()

        # click the button to make the repo public
        self.browser.find_element_by_id('publish').click()

    def make_repo_not_public(self, repo):
        self.browser.find_element_by_id('logo').click()

        # click the collaborators button next to the repo
        xpath = ('(//table/tbody/tr[td/a/text()="{repo}"]/td/a[text()['
                 'contains(.,"collaborator(s)")]])[1]').format(repo=repo)
        self.browser.find_element_by_xpath(xpath).click()

        # click the button to revoke public access
        self.browser.find_element_by_id('unpublish').click()

    def add_collaborator(self, repo, collaborator):
        # assumes the user is logged in
        self.browser.find_element_by_id('logo').click()

        # click the collaborators button next to the repo
        xpath = ('(//table/tbody/tr[td/a/text()="{repo}"]/td/a[text()['
                 'contains(.,"collaborator(s)")]])[1]').format(repo=repo)
        self.browser.find_element_by_xpath(xpath).click()

        # write the new collaborator name
        self.browser.find_element_by_id(
            'collaborator_username').send_keys(collaborator)
        self.browser.find_element_by_id('add_collaborator').click()

    def remove_collaborator(self, repo, collaborator):
        # assumes the user is logged in
        self.browser.find_element_by_id('logo').click()

        # click the collaborators button
        xpath = ('(//table/tbody/tr[td/a/text()="{repo}"]/td/a[text()['
                 'contains(.,"collaborator(s)")]])[1]').format(repo=repo)
        self.browser.find_element_by_xpath(xpath).click()

        # click the remove link next to the user's name
        xpath = ('(//table/tbody/tr/td/ul/li[span/text()="{collaborator}"]'
                 '/a[@title="Remove"])[1]').format(collaborator=collaborator)
        self.browser.find_element_by_xpath(xpath).click()

        # check to make sure that the username isn't still on the page
        page_source = self.browser.page_source
        self.assertFalse(collaborator in page_source)

    def delete_account(self):
        # This requires the browser not to be in mobile mode.
        self.browser.find_element_by_id('id_user_menu').click()
        self.browser.find_element_by_id('id_settings').click()
        self.browser.find_element_by_id('id_delete_acct_button').click()
        self.browser.find_element_by_id('id_delete_confirm_button').click()

        page_source = self.browser.page_source
        self.assertTrue('Account Deleted' in page_source)
