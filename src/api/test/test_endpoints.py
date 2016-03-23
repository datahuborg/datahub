from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.db.manager import DataHubManager
import random
import string
from collections import namedtuple


def random_slug(length):
    return ''.join(
        random.SystemRandom().choice(
            string.ascii_letters) for _ in range(length))


class APIEndpointTests(APITestCase):
    """docstring for APIEndpointTests"""

    def setUp(self):
        self.username = "delete_me_api_test_user"
        self.email = self.username + "@mit.edu"
        self.password = self.username
        self.user = User.objects.create_user(
            self.username, self.email, self.password)
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        # Force close all outstanding db connections to this user's database.
        DataHubManager.remove_user(self.username)


class CurrentUserTests(APIEndpointTests):

    def test_get_user(self):
        url = reverse('api:user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'username': self.username,
            'last_login': None,
            'email': self.email,
            })


class CurrentUserReposTests(APIEndpointTests):

    def test_get_user_repos(self):
        url = reverse('api:user_repos')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'repos': []})


class ReposTests(APIEndpointTests):

    def test_get_repos(self):
        url = reverse('api:repos_all')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'repos': []})


class RepoTests(APIEndpointTests):

    def test_get_repo(self):
        # Make sure it's a 404 when there are no repos.
        repo_name = 'repo_one'
        url = reverse('api:repo',
                      kwargs={'repo_base': self.username,
                              'repo_name': repo_name})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data,
                         {'error_type': 'LookupError',
                          'detail': 'Invalid repository name: repo_one'})

        # Create a repo and make sure it's a 200.
        with DataHubManager(self.username) as manager:
            manager.create_repo(repo_name)

        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         {'files': [],
                          'tables': [],
                          'collaborators': [],
                          'views': [],
                          'cards': [],
                          'owner': {'username': u'delete_me_api_test_user'}})

    def test_patch_repo(self):
        repo_name = 'repo_one'
        url = reverse('api:repo',
                      kwargs={'repo_base': self.username,
                              'repo_name': repo_name})

        # Try renaming a repo that doesn't exist
        response = self.client.patch(
            url, {'new_name': repo_name}, follow=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
                         {'pgcode': '3F000',
                          'error_type': 'ProgrammingError',
                          'detail': 'schema "' + repo_name +
                          '" does not exist\n',
                          'severity': 'ERROR'})

        with DataHubManager(self.username) as manager:
            manager.create_repo(repo_name)

        # Try renaming a repo to its current name
        response = self.client.patch(
            url, {'new_name': 'repo_one'}, follow=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
                         {'pgcode': '42P06',
                          'error_type': 'ProgrammingError',
                          'detail': 'schema "' + repo_name +
                          '" already exists\n',
                          'severity': 'ERROR'})

        # Try renaming for real
        response = self.client.patch(
            url, {'new_name': 'repo_five_thousand'},
            follow=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         {'files': [],
                          'tables': [],
                          'collaborators': [],
                          'views': [],
                          'cards': [],
                          'owner': {'username': u'delete_me_api_test_user'}})

    def test_delete_repo(self):
        # Make sure it's a 404 when there are no repos.
        repo_name = 'repo_one'
        url = reverse('api:repo',
                      kwargs={'repo_base': self.username,
                              'repo_name': repo_name})
        response = self.client.delete(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
                         {'pgcode': '3F000',
                          'error_type': 'ProgrammingError',
                          'detail': 'schema "repo_one" does not exist\n',
                          'severity': 'ERROR'})

        # Create a repo and make sure it's a 200.
        with DataHubManager(self.username) as manager:
            manager.create_repo(repo_name)

        response = self.client.delete(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)


class ReposForUserTests(APIEndpointTests):

    def _expected_response(self, owner, repo_names):
        result = []
        base = 'http://testserver/api/v1/repos/'
        for repo in repo_names:
            result.append({'owner': owner,
                           'href': '{0}{1}/{2}'.format(base, owner, repo),
                           'repo_name': repo})
        return {'repos': result}

    def test_get_repos(self):
        # Expect an empty array when the user has no repos
        url = reverse('api:repos_specific',
                      kwargs={'repo_base': self.username})

        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self._expected_response(
            self.username, []))

        # Add some repos and expect they show up
        repos = ['foo', 'bar', 'baz']
        with DataHubManager(self.username) as manager:
            [manager.create_repo(repo) for repo in repos]
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Sort because the results will be sorted
        self.assertEqual(response.data, self._expected_response(
            self.username, sorted(repos)))

    def test_create_repo(self):
        # Create two repos
        url = reverse('api:repos_specific',
                      kwargs={'repo_base': self.username})

        response = self.client.post(
            url, {'repo_name': 'repo_one'}, follow=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self._expected_response(
            self.username, ['repo_one']))
        response = self.client.post(
            url, {'repo_name': 'repo_two'}, follow=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self._expected_response(
            self.username, ['repo_one', 'repo_two']))


Query = namedtuple('Query', ['sql', 'status_code', 'expect'])


class QueryTests(APIEndpointTests):

    def test_query_with_repo(self):
        repo_name = 'repo_one'
        table_name = 'sandwiches'
        repo_table = repo_name + '.' + table_name
        with DataHubManager(self.username) as manager:
            manager.create_repo(repo_name)

        url = reverse('api:query_with_repo',
                      kwargs={'repo_base': self.username,
                              'repo_name': repo_name})
        queries = [
            Query(sql="""
                  CREATE TABLE """ + table_name + """ (
                      name varchar (255) NOT NULL,
                      deliciousness numeric,
                      is_deep_fried boolean);
                  """,
                  status_code=status.HTTP_200_OK,
                  expect={}),
            Query(sql="SELECT * FROM " + repo_table + ";",
                  status_code=status.HTTP_200_OK,
                  expect=[]),
            Query(sql="INSERT INTO " + repo_table +
                      " VALUES ('reuben', 25, FALSE);",
                  status_code=status.HTTP_200_OK,
                  expect={}),
            Query(sql="SELECT * FROM " + repo_table + ";",
                  status_code=status.HTTP_200_OK,
                  expect=[
                      {'is_deep_fried': False,
                       'deliciousness': 25,
                       'name': 'reuben'}]),
            Query(sql="DROP TABLE " + repo_table,
                  status_code=status.HTTP_200_OK,
                  expect={}),
        ]

        for q in queries:
            response = self.client.post(
                url, {'query': q.sql}, follow=True, format='json')
            print(response.data)
            self.assertEqual(response.status_code, q.status_code)
            self.assertEqual(response.data, q.expect)

    def test_post_query(self):
        repo_name = 'repo_one'
        table_name = 'sandwiches'
        with DataHubManager(self.username) as manager:
            manager.create_repo(repo_name)
        url = reverse('api:query',
                      kwargs={'repo_base': self.username})

        queries = [
            Query(sql="""
                  CREATE TABLE """ + table_name + """ (
                      name varchar (255) NOT NULL,
                      deliciousness numeric,
                      is_deep_fried boolean);
                  """,
                  status_code=status.HTTP_200_OK,
                  expect={}),
            Query(sql="SELECT * FROM " + table_name + ";",
                  status_code=status.HTTP_200_OK,
                  expect=[]),
            Query(sql="INSERT INTO " + table_name +
                      " VALUES ('reuben', 25, FALSE);",
                  status_code=status.HTTP_200_OK,
                  expect={}),
            Query(sql="SELECT * FROM " + table_name + ";",
                  status_code=status.HTTP_200_OK,
                  expect=[
                      {'is_deep_fried': False,
                       'deliciousness': 25,
                       'name': 'reuben'}]),
            Query(sql="DROP TABLE " + table_name,
                  status_code=status.HTTP_200_OK,
                  expect={}),
        ]

        for q in queries:
            response = self.client.post(
                url, {'query': q.sql}, follow=True, format='json')
            print(response.data)
            self.assertEqual(response.status_code, q.status_code)
            self.assertEqual(response.data, q.expect)

    # Test that Accept:text/csv works
    # Test that pagination works
    # Test that responses give metadata
