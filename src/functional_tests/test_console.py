import factory

from django.db.models import signals

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from account.management.commands.createoauthappsandowner import(
    create_oauth2_user, create_console_app)
from .base import FunctionalTest


class ConsoleTest(FunctionalTest):

    @factory.django.mute_signals(signals.pre_save)
    def create_console_oauth(self):
        # django migration operations aren't run consistently by
        # StaticLiveServerTestCase in 1.8/1.9. If they were, we wouldn't need
        # this here (though it wouldn't do anything bad, either.)
        # https://code.djangoproject.com/ticket/23640
        create_oauth2_user(None, None)
        create_console_app(None, None)

    def setUp(self):
        super(ConsoleTest, self).setUp()
        self.create_console_oauth()

    def send_to_console(self, cmd):
        console = self.browser.find_element_by_xpath(
            "//div[@class='cmd']/span[3]")
        console.send_keys(cmd)

    def wait_for_console(self, text, xpath=None):
        if xpath is None:
            xpath = "//div[@class='terminal-output']/div[last()]/div[1]"

        WebDriverWait(self.browser, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, xpath), text)
        )

    def navigate_to_terminal(self):
        self.browser.find_element_by_id('id_user_menu').click()
        self.browser.find_element_by_id('id_launch_terminal').click()

        xpath = "//div[@class='cmd']/span[@class='prompt']"

        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

    def test_create_repos(self):
        good_repo_names = ['nospace', 'alph4numeric', 'middle_underscore']

        self.sign_up_manually()
        self.navigate_to_terminal()

        # make good repos in terminal
        for repo_name in good_repo_names:
            self.send_to_console('mkrepo ' + repo_name + Keys.ENTER)
            self.wait_for_console('success')

        # check to see good repos exist in home
        self.browser.find_element_by_class_name('fa-home').click()
        page_source = self.browser.page_source
        for repo_name in good_repo_names:
            self.assertTrue(repo_name in page_source)

    def test_list_repos(self):
        good_repo_names = ['nospace', 'alph4numeric', 'middle_underscore']

        self.sign_up_manually()
        for repo_name in good_repo_names:
            self.create_repo(repo_name)

        # list repos in terminal
        self.navigate_to_terminal()

        self.send_to_console('ls' + Keys.ENTER)
        self.wait_for_console('3 rows returned')

        # check to see good repos exist
        page_source = self.browser.page_source
        for repo_name in good_repo_names:
            self.assertTrue(repo_name in page_source)

    def test_delete_repos(self):
        good_repo_names = ['nospace', 'alph4numeric', 'middle_underscore']

        self.sign_up_manually()
        for repo_name in good_repo_names:
            self.create_repo(repo_name)

        # delete repos in terminal
        self.navigate_to_terminal()

        for repo_name in good_repo_names:
            self.send_to_console('rm ' + repo_name + Keys.ENTER)
            self.wait_for_console('success')

        # check to see no repos exist in home
        self.browser.find_element_by_class_name('fa-home').click()
        page_source = self.browser.page_source
        for repo_name in good_repo_names:
            self.assertFalse(repo_name in page_source)

    def test_cannot_create_bad_repos(self):
        bad_repo_names = ['one space', '_introUnderscore', 'semi;colon']

        self.sign_up_manually()
        self.navigate_to_terminal()

        # make bad repos in terminal
        for repo_name in bad_repo_names:
            self.send_to_console('mkrepo ' + repo_name + Keys.ENTER)
            self.wait_for_console('failed')

        # check to see bad repos don't exist in home
        self.browser.find_element_by_class_name('fa-home').click()
        page_source = self.browser.page_source
        for repo_name in bad_repo_names:
            self.assertFalse(repo_name in page_source)

    def test_execute_sql(self):
        self.sign_up_manually()
        repo_name = 'my_repo'
        table_name = 'my_table'
        rows = [{'id': 1, 'words': 'one'},
                {'id': 2, 'words': 'two'}]

        # make a repo
        self.create_repo(repo_name)

        # make table using the terminal
        self.navigate_to_terminal()
        self.send_to_console(
            ('CREATE TABLE {repo}.{table}'
                '(id integer, words text)' + Keys.ENTER)
            .format(repo=repo_name, table=table_name))
        self.wait_for_console('success')

        # insert data into table using terminal
        for row in rows:
            self.send_to_console(
                ("INSERT INTO {repo}.{table} "
                    "VALUES ({id}, '{words}')" + Keys.ENTER)
                .format(repo=repo_name,
                        table=table_name,
                        id=row['id'],
                        words=row['words']))
            self.wait_for_console('success')

        # find table and data on the home page
        self.browser.find_element_by_class_name('fa-home').click()
        self.browser.find_element_by_link_text(repo_name).click()
        self.browser.find_element_by_link_text(table_name).click()
        data = self.browser.find_elements_by_xpath(
            "//table[@id='table_data']/tbody/tr")
        self.assertTrue(len(rows) == len(data))

    def test_list_tables(self):
        self.sign_up_manually()
        repo_name = 'repo'
        table_names = ['nospace', 'alph4numeric', 'middle_underscore']

        # make 3 tables in a repo
        self.create_repo(repo_name)
        for table_name in table_names:
            self.create_table(repo_name, table_name)

        # ls repo_name in terminal
        self.navigate_to_terminal()
        self.send_to_console('ls ' + repo_name + Keys.ENTER)
        self.wait_for_console('rows returned')

        # confirm tables are listed
        page_source = self.browser.page_source
        for table_name in table_names:
            self.assertTrue(table_name in page_source)

    def test_describe_tables(self):
        self.sign_up_manually()
        repo_name = 'repo'
        table_name = 'table_name'
        column_names = ['id', 'words']
        column_types = ['integer', 'text']

        # make table in a repo
        self.create_repo(repo_name)
        self.create_table(repo_name, table_name)

        # ls repo_name in terminal
        self.navigate_to_terminal()
        self.send_to_console(
            'desc ' + repo_name + '.' + table_name + Keys.ENTER)
        self.wait_for_console('columns returned')

        # confirm column names are listed
        page_source = self.browser.page_source
        for column_name in column_names:
            self.assertTrue(column_name in page_source)

        # ls repo_name -l in terminal
        self.send_to_console(
            'desc ' + repo_name + '.' + table_name + " -l" + Keys.ENTER)
        self.wait_for_console('columns returned')

        # confirm column names and types are listed
        page_source = self.browser.page_source
        for column_type in column_types:
            self.assertTrue(column_type in page_source)

    def test_connect_to_new_user(self):
        # names
        users = ['delete_me_one', 'delete_me_two', 'i_dont_exist']
        repo_shared = 'one_two'
        repo_user1_only = 'one'
        repo_failed = 'two'

        # user2 signs up and signs out
        self.sign_up_manually(username=users[1], password=None)
        self.sign_out_manually()

        # user1 signs up
        self.sign_up_manually(username=users[0], password=None)

        # user1 makes two repos
        self.create_repo(repo_shared, users[0])
        self.create_repo(repo_user1_only, users[0])

        # user1 adds user2 as a collaborator to repo_shared
        self.add_collaborator(repo_shared, users[1])

        # user1 signs out
        self.sign_out_manually()

        # user2 signs up
        self.sign_in_manually(username=users[1], password=None)

        # user2 tries to connect to user3 and fails
        self.navigate_to_terminal()

        self.send_to_console('connect ' + users[2] + Keys.ENTER)
        self.wait_for_console('failed')

        # user2 successfully connect to user1
        self.send_to_console('connect ' + users[0] + Keys.ENTER)
        self.wait_for_console(
            users[1] + "@" + users[0] + ">", "//div[@class='cmd']/span[1]")

        # user2 lists user1's repos and sees only one
        self.send_to_console('ls' + Keys.ENTER)
        self.wait_for_console('1 rows returned')
        page_source = self.browser.page_source
        self.assertTrue(repo_shared in page_source)

        # user2 tries to make a repo in user1's repo-base and fails
        self.send_to_console('mkrepo ' + repo_failed + Keys.ENTER)
        self.wait_for_console('failed')

        # user2 disconnects from user1 with CTRL+d
        cmd = self.browser.find_element_by_xpath("//div[@class='cmd']/span[3]")
        cmd.send_keys(Keys.CONTROL, 'd')
        self.wait_for_console(
            users[1] + "@" + users[1] + ">", "//div[@class='cmd']/span[1]")

        # user2 lists and sees own repos
        self.send_to_console('ls' + Keys.ENTER)
        self.wait_for_console('0 rows returned')

        # user2 deletes account
        self.delete_account()

        # user1 deletes account
        self.sign_in_manually(username=users[0])
        self.delete_account()
