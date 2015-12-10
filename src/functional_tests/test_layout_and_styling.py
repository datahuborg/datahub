import re
from .base import FunctionalTest


class LayoutAndStylingUnauthenticated(FunctionalTest):

    def test_front_page_content(self):
        # Justin goes to the home page
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # The title of the page includes the word DataHub
        self.assertIn(self.browser.title, "DataHub")

        # The word "Justin" appears in the page
        src = self.browser.page_source
        text_found = re.search(r'Justin', src)
        self.assertNotEqual(text_found, None)

    # skip this test for now. it times out in travis, and takes forever locally
    # def test_front_page_links(self):
        # Justin goes to the home page
    #     self.browser.get(self.server_url)
    #     self.browser.set_window_size(1024, 768)

        # he verifies that all external links on the home page work
    #     self.test_external_links()

    def test_login_signup_pages_content(self):
        # Justin goes to the home page
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # Justin clicks the "Sign In" button
        self.browser.find_element_by_id('id_sign_in').click()
        login_url = self.browser.current_url

        # The word "email" appears in the page
        src = self.browser.page_source
        text_found = re.search(r'email', src)
        self.assertNotEqual(text_found, None)

        # the word "password" appears in the page
        src = self.browser.page_source
        text_found = re.search(r'password', src)
        self.assertNotEqual(text_found, None)

        # Justin realizes that he needs to sign up, and clicks "Sign Up"
        self.browser.find_element_by_id('id_sign_up').click()
        signup_url = self.browser.current_url

        # Login and Signup are on different pages
        self.assertNotEqual(signup_url, login_url)

        # the word "password" appears in the page
        src = self.browser.page_source
        text_found = re.search(r'password', src)
        self.assertNotEqual(text_found, None)


# class LayoutAndStylingLoginPageTest(FunctionalTest):
