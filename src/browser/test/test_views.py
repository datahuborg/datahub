from django.test import TestCase
from django.test import Client

class BrowserPages(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)

    def test_about(self):
        pass

    
        