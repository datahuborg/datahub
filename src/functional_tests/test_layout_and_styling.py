from .base import FunctionalTest
import requests
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
            print("Some links on the front page did not check out")
            self.fail(failing_links)

        # Satisfied, he takes a nap
