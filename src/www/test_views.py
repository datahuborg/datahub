from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

class WwwPages(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)

    def test_index(self):
        response = self.client.get('/www', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class HomePageAuthenticated(TestCase):
    def setUp(self):
        # create the user
        self.username = "test_username"
        self.password = "test_password"
        self.email = "test_email@csail.mit.edu"
        self.user = User.objects.create_user(
            self.username, self.email, self.password)

        # log the user in
        self.client.login(username=self.username, password=self.password)

    def test_authenticated_user_home_redirects_to_browse(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/browse/' + self.username)