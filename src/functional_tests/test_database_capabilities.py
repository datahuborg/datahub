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
            self.browser.find_element_by_class_name('glyphicon-plus').click()

            # type the new repo id
            self.browser.find_element_by_id('new_repo_name').send_keys(name)

            # click create
            self.browser.find_element_by_id('new_repo_create').click()

            # the page says error
            page_source = self.browser.page_source
            self.assertTrue('error' in page_source)

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

    def test_add_collaborator(self):
        alpha_user = 'delete_me_alpha_user'
        beta_user = 'delete_me_beta_user'
        repos = ['ginnjuice', 'beautiful']
        tables = ['dre', 'snoop']

        # make alpha_user
        self.sign_up_manually(username=alpha_user, password=None)
        self.sign_out_manually()

        # make beta_user
        self.sign_up_manually(username=beta_user, password=None)

        # beta_user creates repos and puts tables in them
        for repo in repos:
            self.create_repo(repo, beta_user)

            for table in tables:
                self.create_table_programmatically(repo, table, beta_user)

        # beta_user adds alpha_user as a collabortor to one repo
        self.add_collaborator(repos[0], alpha_user)

        # beta_user logs out
        self.sign_out_manually()

        # alpha_user logs in
        self.sign_in_manually(alpha_user)

        # user 1 can see one of beta_user's repos, but not the other
        # user 1 selects from beta_user's repo. 
