from .base import FunctionalTest


class LoginTest(FunctionalTest):

    def test_create_delete_some_repos(self):
        good_repo_names = ['nospace', 'alph4numeric', 'middle_underscore']

        # Justin signs up and in
        self.sign_up_manually()

        for repo_name in good_repo_names:
            self.create_repo(repo_name)

        for repo_name in good_repo_names:
            self.delete_repo(repo_name)

    def test_cannot_create_bad_repos(self):
        bad_repo_names = ['one space', '_introUnderscore', 'semi;colon']

        # Justin sign up and in
        self.sign_up_manually()

        for name in bad_repo_names:
            # He clicks the add repo button
            self.browser.find_element_by_xpath(
                '(//a[@title="Create a New Repository"])[1]').click()

            # type the new repo id
            self.browser.find_element_by_id('new_repo_name').send_keys(name)

            # click create
            self.browser.find_element_by_id('new_repo_create').click()

            # the page says error
            page_source = self.browser.page_source
            self.assertTrue('Error' in page_source)

            # he goes to the main page
            self.browser.get(self.server_url + '/browse/' + self.username)

            # the repo does not appear
            no_repo = self.browser.find_elements_by_link_text(name)
            self.assertEqual(no_repo, [])

    def test_create_some_tables(self):
        good_table_names = ['nospace', 'alph4numeric', 'middle_underscore']
        repo_name = 'repo_name'

        self.sign_up_manually()
        self.create_repo(repo_name)

        for table_name in good_table_names:
            self.create_table_programmatically(repo_name, table_name)

    def test_create_some_views(self):
        good_view_names = ['nospace', 'alph4numeric', 'middle_underscore']
        repo_name = 'repo_name'
        table_name = 'table_name'

        self.sign_up_manually()
        self.create_repo(repo_name)
        self.create_table_programmatically(repo_name, table_name)

        for view_name in good_view_names:
            self.create_view_programmatically(
                repo_name, table_name, view_name)

    def test_add_remove_collaborator(self):
        eazyE = 'delete_me_eazyE'
        dre = 'delete_me_dre'
        repos = ['efil4zaggin', 'tSoSN', 'sukka']
        tables = ['dopeman', 'thapolice']

        # make eazyE
        self.sign_up_manually(username=eazyE, password=None)
        self.sign_out_manually()

        # make dre
        self.sign_up_manually(username=dre, password=None)

        # dre creates repos and puts tables in them
        for repo in repos:
            self.create_repo(repo, dre)

            for table in tables:
                self.create_table_programmatically(repo, table, dre)

        # dre adds eazyE as a collabortor to one repo
        self.add_collaborator(repos[0], eazyE)

        # dre logs out
        self.sign_out_manually()

        # eazyE logs in
        self.sign_in_manually(eazyE)

        # eazyE goes to the dre url
        self.browser.get(self.server_url + '/browse/' + dre)

        # eazyE does not see repo[1], which is not shared
        try:
            self.browser.find_element_by_link_text(repos[1])
            self.fail()
        except:
            pass

        # eazyE sees ginjuice, which is shared, and clicks on it
        self.browser.find_element_by_link_text(repos[0]).click()

        # eazyE sees that the tables are shared
        table_0 = self.browser.find_element_by_link_text(tables[0])
        table_1 = self.browser.find_element_by_link_text(tables[1])

        self.assertNotEqual(table_0, None)
        self.assertNotEqual(table_1, None)

        # eazyE clicks on a table
        table_0.click()

        # the url matches
        regex = (r'/browse/{user}/{repo}/table/{table}'
                 .format(user=dre, repo=repos[0], table=tables[0]))
        self.assertRegexpMatches(self.browser.current_url, regex)

        # eazyE is a sneaky mother
        # he tries to get early access to dre's "beautiful" repo
        # jerry put him up to
        sneaky_url = ('{base}/browse/{user}/{repo}/tables'
                      .format(base=self.server_url, user=dre, repo=repos[1]))
        self.browser.get(sneaky_url)

        # the page says error.
        page_source = self.browser.page_source
        search_string = 'No table'
        self.assertTrue(search_string in page_source)

        # eazyE gives up. He goes to the homepage, logs out
        # and takes a smoke break.
        self.browser.get(self.server_url + '/browse/' + eazyE)
        self.sign_out_manually()

        # Dre gets word of what's happening. He signs back in
        self.sign_in_manually(dre)

        # And Dre removes eazyE's access
        self.remove_collaborator(repo=repos[0], collaborator=eazyE)

        # Dre then adds eazyE to the repo, sukka
        self.add_collaborator(repos[2], eazyE)

        # Dre heads out. He's got some work to do
        self.sign_out_manually()

        # eazyE logs in and goes to the dre url
        self.sign_in_manually(eazyE)
        self.browser.get(self.server_url + '/browse/' + dre)

        # eazyE doesn't see repos[0], which dre removed his rights to
        try:
            self.browser.find_element_by_link_text(repos[0])
            self.fail()
        except:
            pass

        # eaxyE does see 'sukka' (repo[2])
        self.browser.find_element_by_link_text(repos[2])

        # He tries to sneak into repos[0], but can't get in either.
        sneaky_url = ('{base}/browse/{user}/{repo}/tables'
                      .format(base=self.server_url, user=dre, repo=repos[0]))
        self.browser.get(sneaky_url)

        # the page says error.
        page_source = self.browser.page_source
        search_string = 'No table'
        self.assertTrue(search_string in page_source)

        # eazyE and Dre aren't friends anymore.
