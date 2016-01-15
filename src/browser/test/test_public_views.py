from django.test import TestCase
from django.core.urlresolvers import resolve

from browser.views import home


class BrowserPagesNotRequiringAuth(TestCase):

    def test_home_url_resolves_to_home_func(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_home_url_returns_index_template(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
