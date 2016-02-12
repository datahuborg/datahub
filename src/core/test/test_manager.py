from core.db.manager import DataHubManager

from django.db.models import signals
from django.contrib.auth.models import User
from django.test import TestCase

import factory
from mock import patch, MagicMock


class Initialization(TestCase):

    """Test the correct user is returned."""

    @factory.django.mute_signals(signals.pre_save)
    def setUp(self):
        self.username = "test_username"
        self.password = "_test diff1;cul t passw0rd-"
        self.email = "test_email@csail.mit.edu"
        self.user = User.objects.create_user(
            self.username, self.email, self.password)

        self.mock_connection = self.create_patch(
            'core.db.manager.DataHubConnection')

    def create_patch(self, name):
        # helper method for creating patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def test_initialization(self):
        DataHubManager(user=self.username)

        # username passed
        self.assertEqual(
            self.mock_connection.call_args[1]['user'], self.username)

        # password passed
        self.assertTrue(
            self.mock_connection.call_args[1]['password'] is not None)

        # repo defaults to username
        self.assertEqual(
            self.mock_connection.call_args[1]['repo_base'], self.username)


class BasicOperations(TestCase):

    """Tests basic operations in manager.py."""

    @factory.django.mute_signals(signals.pre_save)
    def setUp(self):
        self.username = "test_username"
        self.password = "_test diff1;cul t passw0rd-"
        self.email = "test_email@csail.mit.edu"
        self.user = User.objects.create_user(
            self.username, self.email, self.password)

        self.mock_connection = self.create_patch(
            'core.db.manager.DataHubConnection')

        self.manager = DataHubManager(user=self.username)

    def create_patch(self, name):
        # helper method for creating patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def test_list_tables(self):
        con_list_tables = self.mock_connection.return_value.list_tables
        self.manager.list_tables('repo')

        self.assertTrue(con_list_tables.called)

    def test_create_table(self):
        con_create_table = self.mock_connection.return_value.create_table
        repo = 'repo'
        table = 'table'
        params = {'id': 'integer', 'words': 'text'}
        self.manager.create_table(repo, table, params)
        self.assertTrue(con_create_table.called)

    def test_list_views(self):
        con_list_views = self.mock_connection.return_value.list_views
        self.manager.list_views('repo')

        self.assertTrue(con_list_views.called)

    def test_list_repos(self):
        con_list_repos = self.mock_connection.return_value.list_repos
        self.manager.list_repos()

        self.assertTrue(con_list_repos.called)

    def test_rename_repo(self):
        con_rename_repo = self.mock_connection.return_value.rename_repo
        # self.mock_Collaborator = self.create_patch(
        #     'inventory.models.Collaborator')

        self.manager = DataHubManager(
            user=self.username, repo_base=self.username)
        self.manager.Collaborator = MagicMock

        self.manager.rename_repo('old_name', 'new_name')
        self.assertTrue(con_rename_repo.called)

    def test_create_repo(self):
        con_create_repo = self.mock_connection.return_value.create_repo
        self.manager.create_repo('repo')

        self.assertTrue(con_create_repo.called)

    def test_delete_repo(self):
        con_delete_repo = self.mock_connection.return_value.delete_repo
        self.manager = DataHubManager(
            user=self.username, repo_base=self.username)
        self.manager.delete_repo('repo')

        self.assertTrue(con_delete_repo.called)
        self.assertEqual(con_delete_repo.call_args[1]['force'], False)

    def test_add_collaborator(self):
        con_add_collab = self.mock_connection.return_value.add_collaborator
        self.create_patch('core.db.manager.User')
        mock_Collaborator = self.create_patch(
            'core.db.manager.Collaborator')
        mock_Collaborator.objects.get_or_create.return_value = (
            MagicMock(), True)

        self.manager.add_collaborator(
            repo='reponame', collaborator='new_collaborator', privileges='select')

        self.assertTrue(con_add_collab.called)
        self.assertEqual(con_add_collab.call_args[1]['repo'], 'reponame')
        self.assertEqual(
            con_add_collab.call_args[1]['collaborator'], 'new_collaborator')
        self.assertEqual(con_add_collab.call_args[1]['privileges'], 'select')

    def test_delete_collaborator(self):
        self.mock_connection.return_value.list_collaborators.return_value = [
            {'username': 'old_collaborator', 'permissions': 'U'},
            {'username': self.username, 'permissions': 'UC'}
            ]
        self.mock_User = self.create_patch('core.db.manager.User')
        self.mock_Collaborator = self.create_patch(
            'core.db.manager.Collaborator')

        con_delete_collab = (self.mock_connection
                             .return_value.delete_collaborator)
        self.manager.delete_collaborator('reponame', 'old_collaborator')

        self.assertTrue(con_delete_collab.called)
        self.assertEqual(con_delete_collab.call_args[1]['repo'], 'reponame')
        self.assertEqual(
            con_delete_collab.call_args[1]['collaborator'], 'old_collaborator')

    def test_get_schema(self):
        con_get_schema = self.mock_connection.return_value.get_schema
        self.manager.get_schema('reponame', 'tablename')

        self.assertTrue(con_get_schema.called)
        self.assertEqual(con_get_schema.call_args[1]['repo'], 'reponame')
        self.assertEqual(con_get_schema.call_args[1]['table'], 'tablename')
