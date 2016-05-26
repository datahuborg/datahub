import os

from mock import patch
import factory

from django.db.models import signals
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.contrib.auth.models import User

import browser.views


class CreateAndDeleteRepo(TestCase):

    @factory.django.mute_signals(signals.pre_save)
    def setUp(self):
        # set up the user. This is the only integration-ey part
        # It's because I had trouble mocking out
        # django.contrib.auth.decorators.login_required
        self.username = "delete_me_test_username"
        self.password = "test_password"
        self.email = "test_email@csail.mit.edu"
        self.user = User.objects.create_user(
            self.username, self.email, self.password)

        # Mock out a repo for the user
        self.repo_name = 'test_repo'
        self.mock_list_repos = self.create_patch(
            'core.db.manager.DataHubManager.list_repos')
        self.mock_list_repos.return_value = {'tuples': [[self.repo_name]]}

        # mock out that they have tables and views, and repo privileges
        self.mock_manager = self.create_patch(
            'browser.views.DataHubManager')
        self.mock_enter = self.mock_manager.return_value.__enter__
        self.mock_manager.return_value.create_repo.return_value = {
            'tuples': [self.repo_name]}
        self.mock_manager.return_value.delete_repo.return_value = {
            'tuples': [self.repo_name]}
        self.mock_manager.has_repo_privilege.return_value = True

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
        self.mock_enter.return_value.create_repo.assert_called_once_with(
            'repo_name')

    def test_create_repo_cannot_happen_on_another_user_acct(self):
        post_object = {'repo': 'repo_name'}
        self.client.post(
            '/create/' + 'bad_username' + '/repo', post_object)

        self.mock_enter.return_value.create_repo.assert_not_called()

    # *** Delete Repos ***

    def test_delete_repo_resolves_to_correct_view_function(self):
        found = resolve('/delete/' + self.username + '/repo/')
        self.assertEqual(found.func, browser.views.repo_delete)

    def test_delete_repo_calls_correct_function(self):
        self.client.post('/delete/' + self.username + '/repo_name')

        self.assertEqual(
            self.mock_enter.return_value.delete_repo.call_count, 1)


class RepoTableCardViews(TestCase):

    @factory.django.mute_signals(signals.pre_save)
    def setUp(self):
        # create the user
        self.username = "delete_me_test_username"
        self.password = "test_password"
        self.email = "test_email@csail.mit.edu"
        self.user = User.objects.create_user(
            self.username, self.email, self.password)

        # Mock out a repo for the user
        self.repo_name = 'test_repo'
        self.mock_list_repos = self.create_patch(
            'core.db.manager.DataHubManager.list_repos')
        self.mock_list_repos.return_value = {'tuples': [[self.repo_name]]}
        # mock out that they have tables and views, and repo privileges
        self.mock_manager = self.create_patch(
            'browser.views.DataHubManager')
        self.mock_enter = self.mock_manager.return_value.__enter__
        self.mock_manager.return_value.list_tables.return_value = {
            'tuples': ['table_1']}
        self.mock_manager.return_value.list_views.return_value = {
            'tuples': ['view_1']}
        self.mock_manager.has_repo_privilege.return_value = True

        # log the user in
        self.client.login(username=self.username, password=self.password)

    def create_patch(self, name):
        # Helper method to create patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    # *** Tables & Views Tab ***

    def test_repo_main_view_redirects_to_tables_view(self):
        response = self.client.get(
            '/browse/' + self.username + "/" + self.repo_name, follow=True)
        self.assertTemplateUsed(response, "repo-browse-tables.html")

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

        mock_list_tables = self.mock_enter.return_value.list_tables
        mock_list_tables.assert_called_once_with(
            self.repo_name)

    # *** Cards Tab ***

    def test_cards_view_returns_correct_function(self):
        found = resolve(
            '/browse/' + self.username + "/" + self.repo_name + "/cards")

        self.assertEqual(found.func, browser.views.repo_cards)

    def test_cards_view_returns_correct_page(self):
        response = self.client.get(
            '/browse/' + self.username + '/' + self.repo_name + "/cards")

        self.assertTemplateUsed(response, 'repo-browse-cards.html')

    def test_card_view_calls_correct_manager_methods(self):
        self.client.get(
            '/browse/%s/%s/card/cardname' % (self.username, self.repo_name))

        self.assertTrue(self.mock_enter.return_value.get_card.called)
        self.assertTrue(self.mock_enter.return_value.paginate_query.called)


class RepoFilesTab(TestCase):

    @factory.django.mute_signals(signals.pre_save)
    def setUp(self):
        # create the user
        self.username = "delete_me_test_username"
        self.password = "test_password"
        self.email = "test_email@csail.mit.edu"
        self.user = User.objects.create_user(
            self.username, self.email, self.password)

        # Mock out a repo for the user
        self.repo_name = 'test_repo'
        self.mock_manager = self.create_patch(
            'browser.views.DataHubManager')

        # make their files folder
        repo_dir = '/user_data/%s/%s' % (self.username, self.repo_name)
        if not os.path.exists(repo_dir):
            os.makedirs(repo_dir)

        # put a file in it, if there wasn't one already.

        # log the user in
        self.client.login(username=self.username, password=self.password)

    def tearDown(self):
        # remove the files folder
        repo_dir = '/user_data/%s/%s' % (self.username, self.repo_name)
        if os.path.exists(repo_dir):
            os.removedirs(repo_dir)

        user_dir = '/user_data/%s' % (self.username)
        if os.path.exists(user_dir):
            os.removedirs(user_dir)

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


class RepoMainPage(TestCase):

    @factory.django.mute_signals(signals.pre_save)
    def setUp(self):
        # create the user
        self.username = "delete_me_test_username"
        self.password = "test_password"
        self.email = "test_email@csail.mit.edu"
        self.user = User.objects.create_user(
            self.username, self.email, self.password)

        # log the user in
        self.client.login(username=self.username, password=self.password)

        # Mock the DataHubManager
        self.mock_manager = self.create_patch(
            'browser.views.DataHubManager')
        self.mock_manager.return_value.list_repos.return_value = {
            'tuples': ['repo_1']}
        self.mock_manager.return_value.list_collaborators.return_value = [
            {'username': 'collaborator_1', 'permissions': 'UC'}]

    def create_patch(self, name):
        # helper method for creating patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def test_repo_main_view_returns_correct_function(self):
        found = resolve('/browse/' + self.username)
        self.assertEqual(found.func, browser.views.user)

    def test_browse_goes_to_repo_func(self):
        found = resolve('/browse/')
        self.assertEqual(found.func, browser.views.user)

    def test_repo_main_view_returns_correct_page(self):
        response = self.client.get('/browse/' + self.username)
        self.assertTemplateUsed(response, 'user-browse.html')


class RepoSettingsPage(TestCase):

    @factory.django.mute_signals(signals.pre_save)
    def setUp(self):
        # create the user
        self.username = "delete_me_test_username"
        self.password = "test_password"
        self.email = "test_email@csail.mit.edu"
        self.user = User.objects.create_user(
            self.username, self.email, self.password)

        # log the user in
        self.client.login(username=self.username, password=self.password)

        # Mock the DataHubManager
        self.mock_manager = self.create_patch(
            'browser.views.DataHubManager')
        self.mock_enter = self.mock_manager.return_value.__enter__
        self.mock_manager.return_value.list_collaborators.return_value = [
            {'username': 'collaborator_1', 'permissions': 'UC'}]

        self.repo_name = "repo_name"

    def create_patch(self, name):
        # helper method for creating patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    # *** Settings Page ***

    def test_repo_settings_resolves_to_correct_function(self):
        found = resolve('/settings/' + self.username + '/' + self.repo_name)
        self.assertEqual(found.func, browser.views.repo_settings)

    def test_repo_settings_returns_correct_page(self):
        response = self.client.get(
            '/settings/' + self.username + '/' + self.repo_name)
        self.assertTemplateUsed(response, 'repo-settings.html')

    # *** Add Collaborators ***

    def test_add_collaborators_resolves_to_correct_function(self):
        add_url = '/collaborator/repo/' + \
            self.username + '/' + self.repo_name + '/add'
        found = resolve(add_url)
        self.assertEqual(found.func, browser.views.repo_collaborators_add)

    def test_add_collaborators_returns_correct_page_and_adds_collab(self):
        add_url = '/collaborator/repo/' + \
            self.username + '/' + self.repo_name + '/add'
        response = self.client.post(
            add_url, {'collaborator_username': 'test_collaborator'},
            follow=True)

        self.assertTemplateUsed(response, 'repo-settings.html')

        mock_add_collab = self.mock_enter.return_value.add_collaborator
        mock_add_collab.assert_called_once_with(
            self.repo_name, 'test_collaborator',
            db_privileges=[], file_privileges=[])


# # to do:
# # mock out login_required
# # share/unshare repo
# # create/delete table
# # table export
# # query

# #


# # test creating tables
# # test uploading files
