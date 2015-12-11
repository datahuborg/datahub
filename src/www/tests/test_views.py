from django.test import TestCase
from django.test import Client


class WwwPages(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)

    def test_index(self):
        response = self.client.get('/www', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
