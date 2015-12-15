from .base import FunctionalTest


class LoginTest(FunctionalTest):

    def test_create_some_repos(self):
        good_repo_names = ['nospace', 'alph4numeric', 'middle_underscore']

        # Justin signs up and in
        self.sign_up_manually()

        for name in good_repo_names:

            # He clicks the add repo button
            self.browser.find_element_by_class_name('glyphicon-plus').click()

            # type the new repo id
            self.browser.find_element_by_id('new_repo_name').send_keys(name)

            # click create
            self.browser.find_element_by_id('new_repo_create').click()

            # check to see that the repo name appears on the page. Click on it.
            self.browser.find_element_by_link_text(name).click()

            # check to see that the url is formatted correctly
            repo_url = self.browser.current_url
            regex = '\/browse\/' + self.username + '\/' + name + '\/tables'
            self.assertRegexpMatches(repo_url, regex)

            # he goes back to the repos page
            self.browser.get(self.server_url + '/browse/' + self.username)

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
