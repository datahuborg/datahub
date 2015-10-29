from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # Justin goes to the home page
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)


        # The title of the page includes the word DataHub

        # The word DataHub appears in the page

        # Justin sees the documentation link, which works

        # Justin sees the github repo link, which works

        # Justin sees the github example code link, which works
