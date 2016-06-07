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
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        error_detail = ('Repo not found. '
                        'You must specify a repo in your query. '
                        'i.e. select * from REPO_NAME.TABLE_NAME. ')
        self.assertEqual(response.data,
                         {'error_type': 'LookupError',
                          'detail': error_detail})

        with DataHubManager(self.username) as manager:
            manager.create_repo(repo_name)

        # Try renaming a repo to its current name
        response = self.client.patch(
            url, {'new_name': 'repo_one'}, follow=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
                         {'error_type': 'ValueError',
                          'detail': 'A repo with that name already exists.'})

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
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        error_detail = ('Repo not found. '
                        'You must specify a repo in your query. '
                        'i.e. select * from REPO_NAME.TABLE_NAME. ')
        self.assertEqual(response.data,
                         {'error_type': 'LookupError',
                          'detail': error_detail})

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


Query = namedtuple(
    'Query', ['sql', 'status_code', 'expect_json', 'expect_csv'])


class QueryTests(APIEndpointTests):

    def _queries(self, table):
        return [
            Query(sql="""CREATE TABLE """ + table + """ (
                      name varchar (255) NOT NULL,
                      deliciousness numeric,
                      is_deep_fried boolean);
                  """,
                  status_code=status.HTTP_200_OK,
                  expect_json=[{'status': 'success'}],
                  expect_csv=''),
            Query(sql="SELECT * FROM " + table + ";",
                  status_code=status.HTTP_200_OK,
                  expect_json=[],
                  expect_csv=''),
            Query(sql="INSERT INTO " + table +
                      " VALUES ('reuben', 25, FALSE);",
                  status_code=status.HTTP_200_OK,
                  expect_json=[{'status': 'success'}],
                  expect_csv=''),
            Query(sql="SELECT * FROM " + table + ";",
                  status_code=status.HTTP_200_OK,
                  expect_json=[
                      {'is_deep_fried': False,
                       'deliciousness': 25,
                       'name': 'reuben'}],
                  expect_csv="deliciousness,is_deep_fried,name\r\n"
                             "25,False,reuben"),
            Query(sql="DROP TABLE " + table,
                  status_code=status.HTTP_200_OK,
                  expect_json=[{'status': 'success'}],
                  expect_csv=''),
        ]

    def test_post_query_with_repo(self):
        repo_name = 'repo_one'
        table_name = 'sandwiches'
        repo_table = repo_name + '.' + table_name
        queries = self._queries(repo_table)

        with DataHubManager(self.username) as manager:
            manager.create_repo(repo_name)

        url = reverse('api:query_with_repo',
                      kwargs={'repo_base': self.username,
                              'repo_name': repo_name})

        for q in queries:
            response = self.client.post(
                url, {'query': q.sql}, follow=True, format='json')
            self.assertEqual(response.status_code, q.status_code)
            self.assertEqual(response.data.get('rows'), q.expect_json)

    def test_post_query_csv_accept_header(self):
        repo_name = 'repo_one'
        table_name = 'sandwiches'
        repo_table = repo_name + '.' + table_name
        queries = self._queries(repo_table)

        with DataHubManager(self.username) as manager:
            manager.create_repo(repo_name)
        url = reverse('api:query',
                      kwargs={'repo_base': self.username})

        for q in queries:
            # import pdb; pdb.set_trace()
            response = self.client.post(
                url, {'query': q.sql}, follow=True, format='json',
                **{'HTTP_ACCEPT': 'text/csv'})
            self.assertEqual(response.status_code, q.status_code)
            self.assertEqual(response.content.strip(), q.expect_csv)

    def test_post_query_json_accept_header(self):
        repo_name = 'repo_one'
        table_name = 'sandwiches'
        repo_table = repo_name + '.' + table_name
        queries = self._queries(repo_table)

        with DataHubManager(self.username) as manager:
            manager.create_repo(repo_name)
        url = reverse('api:query',
                      kwargs={'repo_base': self.username})

        for q in queries:
            # import pdb; pdb.set_trace()
            response = self.client.post(
                url, {'query': q.sql}, follow=True, format='json',
                **{'HTTP_ACCEPT': 'application/json'})
            self.assertEqual(response.status_code, q.status_code)
            self.assertEqual(response.data.get('rows'), q.expect_json)

    def test_post_query_csv_suffix(self):
        repo_name = 'repo_one'
        table_name = 'sandwiches'
        repo_table = repo_name + '.' + table_name
        queries = self._queries(repo_table)

        with DataHubManager(self.username) as manager:
            manager.create_repo(repo_name)
        url = reverse('api:query',
                      kwargs={'repo_base': self.username}) + '.csv'

        for q in queries:
            # import pdb; pdb.set_trace()
            response = self.client.post(
                url, {'query': q.sql}, follow=True, format='json')
            self.assertEqual(response.status_code, q.status_code)
            self.assertEqual(response.content.strip(), q.expect_csv)

    def test_post_query_json_suffix(self):
        repo_name = 'repo_one'
        table_name = 'sandwiches'
        repo_table = repo_name + '.' + table_name
        queries = self._queries(repo_table)

        with DataHubManager(self.username) as manager:
            manager.create_repo(repo_name)
        url = reverse('api:query',
                      kwargs={'repo_base': self.username}) + '.json'

        for q in queries:
            # import pdb; pdb.set_trace()
            response = self.client.post(
                url, {'query': q.sql}, follow=True, format='json')
            self.assertEqual(response.status_code, q.status_code)
            self.assertEqual(response.data.get('rows'), q.expect_json)

    # Test that pagination works
    # Test that responses give metadata
