import hashlib
from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import resolve
from django.contrib.auth.models import User
from core.db.manager import DataHubManager
import browser.views
from mock import MagicMock, patch


# tests below this comment require authentication
# if these fail because a role/database already exists
# you may need to log into postgres and
# drop database username;
# drop role username;

# These are really more integration than unit tests, since they add data
# into the database. There's not a good way around this for now.

class CreateAndDeleteRepo(TestCase):

    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)

        # create the user
        self.username = "test_username"
        self.password = "test_password"
        self.email = "test_email@csail.mit.edu"
        self.user = User.objects.create_user(
            self.username, self.email, self.password)
        self.hashed_password = hashlib.sha1(self.password).hexdigest()

        # create user's database
        DataHubManager.create_user(
            username=self.username, password=self.hashed_password)

        # log the user in
        self.client.login(username=self.username, password=self.password)

    def tearDown(self):
        # remove the postgres db. User will log out automatically.
        DataHubManager.remove_user_and_database(username=self.username)

    # *** Create Repos ***

    def test_create_repo_resolves_to_correct_view_function(self):
        try:
            found = resolve('/create/' + self.username + '/repo/')
        except:
            self.fail(
                "exception at test_create_repo_resolves_to_create_func hit")

        self.assertEqual(found.func, browser.views.repo_create)

    def test_create_repo_returns_correct_page(self):
        try:
            login_credentials = {'login_id': self.username,
                                 'login_password': self.password}

            response = self.client.get(
                '/create/' + self.username + '/repo', follow=True)
        except:
            self.fail("exception at test_create_repo_returns_correct_page hit")

        self.assertTemplateUsed(response, 'repo-create.html')

    @patch('core.db.manager.DataHubManager.create_repo')
    def test_create_repo_calls_correct_function(self, mock_create_repo):
        # The method checks to make sure that the correct method is called.

        try:
            # create the new repo
            mock_create_repo.return_value = None
            post_object = {'repo': 'repo_name'}
            self.client.post('/create/' + self.username + '/repo', post_object)

        except:
            self.fail("exception at test_create_repo_creates_a_repo")
        mock_create_repo.assert_called_once_with('repo_name')

    @patch('core.db.manager.DataHubManager.create_repo')
    def test_create_repo_cannot_happen_on_another_user_acct(self, mock_create_repo):
        try:
            # create the new repo
            mock_create_repo.return_value = None
            post_object = {'repo': 'repo_name'}
            self.client.post(
                '/create/' + 'bac_username' + '/repo', post_object)

        except:
            self.fail("exception at test_create_repo_creates_a_repo")

        mock_create_repo.assert_not_called()

    # *** Delete Repos ***

    def test_delete_repo_resolves_to_correct_view_function(self):
        try:
            found = resolve('/delete/' + self.username + '/repo/')
        except:
            self.fail(
                "exception at test_delete_repo_resolves_to_correct_view_function")

        self.assertEqual(found.func, browser.views.repo_delete)

    @patch('core.db.manager.DataHubManager.delete_repo')
    def test_delete_repo_calls_correct_function(self, mock_delete_repo):
        try:
            mock_delete_repo.return_value = None
            self.client.post('/delete/' + self.username + '/repo_name')

        except:
            self.fail('exception at test_delete_repo_calls_correct_function')

        self.assertEqual(mock_delete_repo.call_count, 1)

    @patch('core.db.manager.DataHubManager.delete_repo')
    def test_delete_cannot_happen_on_another_user_acct(self, mock_delete_repo):
        try:
            mock_delete_repo.return_value = None
            self.client.post('/delete/' + 'wrong_username' + '/repo_name')

        except:
            self.fail('exception at test_delete_repo_calls_correct_function')

        mock_delete_repo.assert_not_called()


# class RepoFeaturePages(TestCase):

#     def setUp(self):
#         self.client = Client(enforce_csrf_checks=False)

#         # create the user
#         self.username = "test_username"
#         self.password = "test_password"
#         self.email = "test_email@csail.mit.edu"
#         self.user = User.objects.create_user(
#             self.username, self.email, self.password)
#         self.hashed_password = hashlib.sha1(self.password).hexdigest()

#         # create user's database
#         DataHubManager.create_user(
#             username=self.username, password=self.hashed_password)

#         # create a repo
#         self.repo_base = 'test_repo'
#         DataHubManager.create_repo(repo=self.repo_base)

#         # log the user in
#         self.client.login(username=self.username, password=self.password)

#     def tearDown(self):
#         DataHubManager.remove_user_and_database(username=self.username)
#         # remove the postgres db. User will log out automatically.

#     def test_table_view_returns_correct_function(self):
#         pass
#         self.assertEqual(1, 1)
        # try:
        #     found = resolve('/browse/' + self.username + "/" + self.repo_base + "/tables")
        # except:
        #     self.fail("exception at test_create_repo_resolves_to_create_func hit")

        # self.assertEqual(found.func, browser.views.table)

    # def test_create_table(self):
    #     pass

    # def createCard(self):
    #     pass

    # def createAnotation(self):
    #     pass

    # def deleteRepo(self):
    #     pass

    # def deleteCard(self):
    #     pass

    # def deleteAnnotation(self):
    #     pass
