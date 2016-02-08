import factory
from mock import patch, MagicMock

from django.test import TestCase

from psycopg2 import ProgrammingError
from ..serializer import RepoSerializer


class RepoSerializerTests(TestCase):
    """Test RepoSerializer methods"""

    def setUp(self):
        self.username = "delete_me_username"
        self.repo_base = "delete_me_repo_base"
        self.password = "delete_me_password"

        self.mock_manager = self.create_patch(
            'api.serializer.DataHubManager')
        self.serializer = RepoSerializer(
            username=self.username, repo_base=self.repo_base)

    def create_patch(self, name):
        # helper method for creating patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def test_create_repo_happy_path(self):
        mock_manager_create_repo = self.mock_manager.return_value.create_repo

        success = self.serializer.create_repo('new_repo_name')

        self.assertTrue(mock_manager_create_repo.called)
        self.assertTrue(success)

    def test_create_repo_sad_path(self):
        mock_manager_create_repo = self.mock_manager.return_value.create_repo
        mock_manager_create_repo.side_effect = ProgrammingError

        success = self.serializer.create_repo('new_repo_name')
        self.assertFalse(success)

    def test_delete_repo_happy_path(self):
        mock_manager_delete_repo = self.mock_manager.return_value.delete_repo

        success = self.serializer.delete_repo('repo_to_be_deleted')
        self.assertTrue(mock_manager_delete_repo.called)
        self.assertTrue(success)

    def test_delete_repo_sad_path(self):
        mock_manager_delete_repo = self.mock_manager.return_value.delete_repo
        mock_manager_delete_repo.side_effect = ProgrammingError

        success = self.serializer.delete_repo('repo_to_be_deleted')
        self.assertFalse(success)

    def test_rename_repo_happy_path(self):
        mock_manager_rename_repo = self.mock_manager.return_value.rename_repo

        success = self.serializer.rename_repo('old_repo_name', 'new_repo_name')

        self.assertTrue(mock_manager_rename_repo.called)
        self.assertTrue(success)

    def test_rename_repo_sad_path(self):
        mock_manager_rename_repo = self.mock_manager.return_value.rename_repo
        mock_manager_rename_repo.side_effect = ProgrammingError

        success = self.serializer.rename_repo('old_repo_name', 'new_repo_name')
        self.assertFalse(success)

    def test_user_owned_repos(self):
        mock_manager_list_repos = self.mock_manager.return_value.list_repos
        mock_manager_list_repos.return_value = ['repo_1', 'repo_2']

        mock_list_collabs = self.mock_manager.return_value.list_collaborators
        mock_list_collabs.return_value = ['collabs']

        repos = self.serializer.user_owned_repos()
        expected_response = {
            'repos': [
                {'repo_name': 'repo_1',
                 'permissions': 'ALL',
                 'collaborators': ['collabs'],
                 'owner': self.username},
                {'repo_name': 'repo_2',
                 'permissions': 'ALL',
                 'collaborators': ['collabs'],
                 'owner': self.username},
            ]
        }

        self.assertEqual(repos, expected_response)

    def test_specific_collab_repos(self):
        # remove the limitation on test comparisons
        self.maxDiff = None

        # mock out user
        mock_User = self.create_patch('api.serializer.User.objects.get')
        mock_User.return_value = 'mock_user'

        # create a MagicMock object for list_colaborators to return
        repo_obj_mock = MagicMock
        repo_obj_mock.repo_name = 'repo_name'
        repo_obj_mock.permission = 'repo_permission'
        repo_obj_mock.repo_base = 'repo_base'

        # mock out collab
        mock_Collab = self.create_patch(
            'api.serializer.Collaborator.objects.filter')
        mock_Collab.return_value = [repo_obj_mock, repo_obj_mock]

        # mock out the manager's list_collaborators method
        mock_list_collabs = self.mock_manager.return_value.list_collaborators
        mock_list_collabs.return_value = ['collabs']

        repos = self.serializer.specific_collab_repos('narf')

        expected_response = {
            'repos': [
                {'repo_name': 'repo_name',
                 'permissions': 'repo_permission',
                 'collaborators': ['collabs'],
                 'owner': 'repo_base'},
                {'repo_name': 'repo_name',
                 'permissions': 'repo_permission',
                 'collaborators': ['collabs'],
                 'owner': 'repo_base'},
            ]
        }

        self.assertEqual(repos, expected_response)

    def test_user_accessible_repos(self):
        # mock out the results of different serializer methods
        mock_user_owned = self.create_patch(
            'api.serializer.RepoSerializer.user_owned_repos')
        mock_user_owned.return_value = {'repos': ['user_owned_repos']}

        # mock out the results of different serializer methods
        mock_all_collab = self.create_patch(
            'api.serializer.RepoSerializer.all_collab_repos')
        mock_all_collab.return_value = {'repos': ['all_collab_repos']}

        response = self.serializer.user_accessible_repos()
        expected_response = {
            'repos': ['user_owned_repos', 'all_collab_repos']
            }

        self.assertEqual(response, expected_response)


# self.manager = 139930597827152
# self.mock_manager = 139930608555664
# self.mock_manager.create_repo = 139930596321168
