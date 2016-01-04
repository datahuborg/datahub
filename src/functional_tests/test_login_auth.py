from .base import FunctionalTest


class LoginTest(FunctionalTest):

    def test_sign_in_bad_user(self):
        # Justin has not created an account, but he tries to sign in anyway
        self.sign_in_manually()
        justin_url = self.browser.current_url
        self.assertNotRegexpMatches(justin_url, self.username)

    def test_register_user_manually_sign_in_and_delete(self):
        # User visits DataHub homepage.
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # Justin clicks "Sign Up"
        self.browser.find_element_by_id('id_sign_up')

        # Justin registers a new account
        self.sign_up_manually()

        # The URL bar now now shows Justin's username
        justin_url = self.browser.current_url

        self.assertRegexpMatches(justin_url, self.username)

        # Justin clicks on the menu item with his name
        self.browser.find_element_by_id('id_user_menu').click()

        # Justin signs out
        self.browser.find_element_by_id('id_sign_out').click()

        # User is redirected back to DataHub homepage.
        justin_url = self.browser.current_url
        self.assertRegexpMatches(justin_url, 'www')

        # Justin is able to sign back in
        self.sign_in_manually()
        justin_url = self.browser.current_url
        self.assertRegexpMatches(justin_url, self.username)

        # DataHub deletes his user and database, somewhat vindictively
        # self.delete_user(self.username)

        # Justin doesn't like DataHub
        # Justin goes to the settings page
        # self.browser.find_element_by_id('id_settings').click()

        # Justin deletes his account
        # self.delete_account()

        # Justin is now logged out
        # justin_url = self.browser.current_url
        # self.assertRegexpMatches(justin_url, 'logout')

        # Justin cannot sign back in
        # self.sign_in_manually()
        # justin_url = self.browser.current_url
        # self.assertNotRegex(justin_url, self.username)

    # def test_justin_hacks_the_planet(self):
    #     pass
        # Justin is hacking the planet
        # Justin sneakily registers his username again

        # His data does not reappear

        # Justin has messed with the best. He dies like the rest.

    # def delete_account(self):
    #     pass
