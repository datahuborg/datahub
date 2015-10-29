from .base import FunctionalTest
import re


class LayoutAndStylingTest(FunctionalTest):

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

    def test_front_page_links(self):
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768) 

        # he verifies that all external links on the home page work
        self.test_external_links()

        # Satisfied, he takes a nap
