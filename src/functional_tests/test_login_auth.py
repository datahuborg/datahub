from .base import FunctionalTest


class LoginTest(FunctionalTest):

    def test_register_user_manually_sign_in_and_delete(self):
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)
        
        # Justin clicks "Sign Up"
        self.browser.find_element_by_id('id_sign_up')
        import pdb; pdb.set_trace()
        # Justin registers a new account
        self.sign_up_manually()

        # The URL bar now now shows Justin's username
        justin_url = self.browser.current_url
        self.assertRegex(justin_url, self.username)

        # Justin is signs out
        self.browser.find_element_by_id('id_sign_out')

        # The URL bar now shows logout
        justin_url = self.browser.current_url
        self.assertRegex(justin_url, 'logout')

        # Justin is able to sign back in
        self.sign_in_manually()
        self.assertRegex(justin_url, self.username)

        # Justin doesn't like DataHub
        # Justin goes to the settings page
        self.browser.find_element_by_id('id_settings').click()

        # Justin deletes his account
        self.delete_account()

        # Justin is now logged out
        justin_url = self.browser.current_url
        self.assertRegex(justin_url, 'logout')

        # Justin cannot sign back in
        self.sign_in_manually()
        self.assertNotRegex(justin_url, self.username)


    def test_justin_hacks_the_planet(self):
        pass
        # Justin is hacking the planet
        ## Justin sneakily registers his username again

        # His data does not reappear

        # Justin has messed with the best. He does like the rest.



    def delete_account(self):
        pass




