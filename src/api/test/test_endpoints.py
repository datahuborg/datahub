from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.db.manager import DataHubManager
from core.db.backend.pg import _close_all_connections
import random
import string


def random_slug(length):
    return ''.join(
        random.SystemRandom().choice(
            string.ascii_letters) for _ in range(length))


class APIEndpointTests(APITestCase):
    """docstring for APIEndpointTests"""

    def setUp(self):
        self.username = "asldbhjdefhijklmnopqr"
        self.email = self.username + "@mit.edu"
        self.password = self.username
        self.user = User.objects.create_user(
            self.username, self.email, self.password)
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        # Force close all outstanding db connections to this user's database.
        _close_all_connections(repo_base=self.username)
        DataHubManager.remove_user(self.username)


class UserEndpointTests(APIEndpointTests):

    def test_get_user(self):
        url = reverse('api:user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'username': self.username,
            'last_login': None,
            'email': self.email,
            })


class UserReposEndpointTests(APIEndpointTests):

    def test_get_user_repos(self):
        # import pdb; pdb.set_trace()
        url = reverse('api:user_repos')
        response = self.client.get(url, follow=True)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'repos': []})


class ReposEndpointTests(APIEndpointTests):

    def test_get_repos(self):
        # url = reverse('api:repos_all')
        # response = self.client.get(url, follow=True)
        # print(response.data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data, {'repos': []})
        pass

    # def test_create_repo(self):
    #     url = reverse('api:repos_all')
    #     data = {'repo_name': 'repo_one'}
    #     response = self.client.post(url, data, follow=True, format='json')
    #     print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data, {'repos': []})
