import os
import hashlib
from mock import MagicMock, patch

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.contrib.auth.models import User

from core.db.manager import DataHubManager
import browser.views


# tests below this comment require authentication
# if these fail because a role/database already exists
# you may need to log into postgres and
# drop database username;
# drop role username;

# These are really more integration than unit tests, since they add data
# into the database. There's not a good way around this for now.

class CreateAndDeleteRepo(TestCase):

    def setUp(self):
        # create the user
        self.username = "test_username"
        self.password = "test_password"
        self.email = "test_email@csail.mit.edu"
        self.user = User.objects.create_user(
            self.username, self.email, self.password)
        self.hashed_password = hashlib.sha1(self.password).hexdigest()

        # Mock out a repo for the user
        self.repo_name = 'test_repo'
        self.mock_list_repos = self.create_patch(
            'core.db.manager.DataHubManager.list_repos')
        self.mock_list_repos.return_value = {'tuples': [[self.repo_name]]}

        # mock out that they have tables and views, and repo priviledges
        self.mock_DataHubManager = self.create_patch(
            'browser.views.DataHubManager')
        self.mock_DataHubManager.return_value.create_repo.return_value = {
            'tuples': [self.repo_name]}
        self.mock_DataHubManager.return_value.delete_repo.return_value = {
            'tuples': [self.repo_name]}
        
            
        self.mock_DataHubManager.has_repo_privilege.return_value = {
            'tuples': [[True]]}

       # log the user in
        self.client.login(username=self.username, password=self.password)

    def tearDown(self):
        pass
        # remove the postgres db. User will log out automatically.

    def create_patch(self, name):
        # helper method for creating patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    # *** Create Repos ***

    def test_create_repo_resolves_to_correct_view_function(self):
        found = resolve('/create/' + self.username + '/repo/')

        self.assertEqual(found.func, browser.views.repo_create)

    def test_create_repo_returns_correct_page(self):
        response = self.client.get(
            '/create/' + self.username + '/repo', follow=True)

        self.assertTemplateUsed(response, 'repo-create.html')

    def test_create_repo_calls_correct_function(self):
        # The method checks to make sure that the correct method is called.
        post_object = {'repo': 'repo_name'}
        self.client.post('/create/' + self.username + '/repo', post_object)

        self.mock_DataHubManager.return_value.create_repo.assert_called_once_with(
            'repo_name')

    def test_create_repo_cannot_happen_on_another_user_acct(self):
        post_object = {'repo': 'repo_name'}
        self.client.post(
            '/create/' + 'bac_username' + '/repo', post_object)

        self.mock_DataHubManager.return_value.create_repo.assert_not_called()

    # *** Delete Repos ***

    def test_delete_repo_resolves_to_correct_view_function(self):
        found = resolve('/delete/' + self.username + '/repo/')
        self.assertEqual(found.func, browser.views.repo_delete)

    def test_delete_repo_calls_correct_function(self):
        self.client.post('/delete/' + self.username + '/repo_name')

        self.assertEqual(self.mock_DataHubManager.return_value.delete_repo.call_count, 1)

    def test_delete_cannot_happen_on_another_user_acct(self):
        self.client.post('/delete/' + 'wrong_username' + '/repo_name')

        self.mock_DataHubManager.return_value.delete_repo.assert_not_called()


class RepoTablesAndViewsTab(TestCase):

    def setUp(self):
        # create the user
        self.username = "test_username"
        self.password = "test_password"
        self.email = "test_email@csail.mit.edu"
        self.user = User.objects.create_user(
            self.username, self.email, self.password)
        self.hashed_password = hashlib.sha1(self.password).hexdigest()

        # Mock out a repo for the user
        self.repo_name = 'test_repo'
        self.mock_list_repos = self.create_patch(
            'core.db.manager.DataHubManager.list_repos')
        self.mock_list_repos.return_value = {'tuples': [[self.repo_name]]}

        # mock out that they have tables and views, and repo priviledges
        self.mock_DataHubManager = self.create_patch(
            'browser.views.DataHubManager')
        self.mock_DataHubManager.return_value.list_tables.return_value = {
            'tuples': ['table_1']}
        self.mock_DataHubManager.return_value.list_views.return_value = {
            'tuples': ['view_1']}
        self.mock_DataHubManager.has_repo_privilege.return_value = {
            'tuples': [[True]]}

       # log the user in
        self.client.login(username=self.username, password=self.password)

    def create_patch(self, name):
        # Helper method to create patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    # *** Tables & Views Tab ***

    def test_table_view_returns_correct_function(self):
        found = resolve(
            '/browse/' + self.username + "/" + self.repo_name + "/tables")
        self.assertEqual(found.func, browser.views.repo_tables)

    def test_table_view_returns_correct_page(self):
        response = self.client.get(
            '/browse/' + self.username + '/' + self.repo_name + "/tables")
        self.assertTemplateUsed(response, 'repo-browse-tables.html')

    def test_table_view_calls_correct_manager_functions(self):
        self.client.get(
            '/browse/' + self.username + '/' + self.repo_name + "/tables")

        self.mock_DataHubManager.return_value.list_tables.assert_called_once_with(
            self.repo_name)
        self.mock_DataHubManager.return_value.list_tables.assert_called_once_with(
            self.repo_name)
        self.mock_DataHubManager.has_repo_privilege.assert_called_once_with(
            self.username, self.username, self.repo_name, 'USAGE')

    def test_table_view_throws_err_on_wrong_user(self):
        # set up has_repo_priviledge to raise an exception
        self.mock_DataHubManager.has_repo_privilege.return_value = False

        self.client.get(
            '/browse/' + 'wrong_username' + '/' + self.repo_name +
            "/tables"
        )

        self.mock_DataHubManager.has_repo_privilege.assert_called_once_with(
            self.username, 'wrong_username', self.repo_name, 'USAGE')
        self.mock_DataHubManager.return_value.list_tables.assert_not_called()
        self.mock_DataHubManager.return_value.list_views.assert_not_called()

    # *** Cards Tab ***

    # def test_cards_view_returns_correct_function(self):
    #     try:
    #         found = resolve(
    #             '/browse/' + self.username + "/" + self.repo_name + "/cards")
    #     except:
    #         self.fail("exception at test_create_repo_resolves_to_create_func")

    #     self.assertEqual(found.func, browser.views.repo_files)

    # def test_cards_view_returns_correct_page(self):
    #     try:
    #         response = self.client.get(
    #             '/browse/' + self.username + '/' + self.repo_name + "/cards")
    #     except:
    #         self.fail("exception at test_table_view_returns_correct_page")
    # if this fails, it's likely because the folder for user data
    # is hardcoded as '/user_data/USERNAME/REPO', and the app doesn't
    # have permission to write there.
    # You may have to chmod the folder

    #     self.assertTemplateUsed(response, 'repo-browse-files.html')


class RepoFilesTab(TestCase):

    def setUp(self):
        # create the user
        self.username = "test_username"
        self.password = "test_password"
        self.email = "test_email@csail.mit.edu"
        self.user = User.objects.create_user(
            self.username, self.email, self.password)
        self.hashed_password = hashlib.sha1(self.password).hexdigest()

        # Mock out a repo for the user
        self.repo_name = 'test_repo'
        self.mock_list_repos = self.create_patch(
            'core.db.manager.DataHubManager.list_repos')
        self.mock_list_repos.return_value = {'tuples': [[self.repo_name]]}

        # mock out that they have priviledges
        self.mock_has_repo_privilege = self.create_patch(
            'core.db.manager.DataHubManager.has_repo_privilege')
        self.mock_has_repo_privilege.return_value = {'tuples': [[[True]]]}

        # make their files folder
        repo_dir = '/user_data/%s/%s' % (self.username, self.repo_name)
        if not os.path.exists(repo_dir):
            os.makedirs(repo_dir)

        # put a file in it, if there wasn't one already.

        # log the user in
        self.client.login(username=self.username, password=self.password)

    # *** Files Tab ***

    def create_patch(self, name):
        # helper method for creating patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def test_files_view_returns_correct_function(self):
        found = resolve(
            '/browse/' + self.username + "/" + self.repo_name + "/files")

        self.assertEqual(found.func, browser.views.repo_files)

    def test_files_view_returns_correct_page(self):
        response = self.client.get(
            '/browse/' + self.username + '/' + self.repo_name + "/files")

        self.assertTemplateUsed(response, 'repo-browse-files.html')

    def test_files_view_checks_for_repo_permission(self):
        self.assertEqual(self.mock_has_repo_privilege.called, False)
        self.client.get(
            '/browse/' + self.username + '/' + self.repo_name + "/files")

        self.mock_has_repo_privilege.assert_called_once_with(
            'test_username', 'test_username', 'test_repo', 'USAGE')

    def test_files_view_returns_existing_files(self):
        response = self.client.get(
            '/browse/' + self.username + '/' + self.repo_name + "/files")
        pass

    def test_files_view_cannot_be_accessed_by_wrong_user(self):
        pass

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

# to do:
# finish converting to mocked DataHubManager
# share repo
# test creating tables
# test all of cards
# test uploading files
