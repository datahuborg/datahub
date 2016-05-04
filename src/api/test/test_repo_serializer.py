from mock import patch, MagicMock

from django.test import TestCase

from ..serializer import RepoSerializer


class RepoSerializerTests(TestCase):
    """Test RepoSerializer methods"""

    def setUp(self):
        self.username = "delete_me_username"
        self.repo_base = "delete_me_repo_base"
        self.password = "delete_me_password"

        self.mock_manager = self.create_patch(
            'api.serializer.DataHubManager')
        self.mock_reverse = self.create_patch(
            'api.serializer.reverse')
        self.mock_reverse.return_value = ('mock_url')
        self.serializer = RepoSerializer(
            username=self.username, repo_base=self.repo_base)

    def create_patch(self, name):
        # helper method for creating patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def test_create_repo(self):
        mock_manager_create_repo = self.mock_manager.return_value.create_repo
        mock_manager_create_repo.return_value = True

        success = self.serializer.create_repo('new_repo_name')
        self.assertTrue(mock_manager_create_repo.called)
        self.assertEqual(success, True)

    def test_delete_repo(self):
        mock_manager_delete_repo = self.mock_manager.return_value.delete_repo
        mock_manager_delete_repo.return_value = True

        success = self.serializer.delete_repo('repo_to_be_deleted')
        self.assertTrue(mock_manager_delete_repo.called)
        self.assertEqual(success, True)

    def test_rename_repo(self):
        mock_manager_rename_repo = self.mock_manager.return_value.rename_repo
        mock_manager_rename_repo.return_value = True

        success = self.serializer.rename_repo('old_repo_name', 'new_repo_name')
        self.assertTrue(mock_manager_rename_repo.called)
        self.assertEqual(success, True)

    def test_user_owned_repos(self):
        mock_manager_list_repos = self.mock_manager.return_value.list_repos
        mock_manager_list_repos.return_value = ['repo_1', 'repo_2']

        mock_list_collabs = self.mock_manager.return_value.list_collaborators
        mock_list_collabs.return_value = ['collabs']

        repos = self.serializer.user_owned_repos()
        expected_response = {
            'repos': [
                {'owner': 'delete_me_repo_base',
                 'href': 'mock_url',
                 'repo_name': 'repo_1'},
                {'owner': 'delete_me_repo_base',
                 'href': 'mock_url',
                 'repo_name': 'repo_2'}
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

        repos = self.serializer.specific_collab_repos('foo')

        expected_response = {
            'repos': [
                {'owner': 'repo_base',
                 'href': 'mock_url',
                 'repo_name': 'repo_name'},
                {'owner': 'repo_base',
                 'href': 'mock_url',
                 'repo_name': 'repo_name'}
            ]}

        self.assertEqual(repos, expected_response)

    def test_public_repos(self):
        mock_collab = MagicMock()
        mock_collab.repo_name = 'repo_name'
        mock_collab.repo_base = 'repo_base'

        mock_Manager = self.create_patch(
            'api.serializer.DataHubManager')
        mock_Manager.list_public_repos.return_value = [mock_collab]

        expected_response = {
            'repos': [
                {"owner": "repo_base",
                 "href": "mock_url",
                 "repo_name": "repo_name"}]
        }
        res = self.serializer.public_repos()
        self.assertEqual(res, expected_response)

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

    def test_all_collab_repos(self):
        repo_obj_mock = MagicMock
        repo_obj_mock.repo_name = 'repo_name'
        repo_obj_mock.permission = 'repo_permission'
        repo_obj_mock.repo_base = 'repo_base'

        mock_manager_return = self.mock_manager.return_value
        mock_collab_repos = mock_manager_return.list_collaborator_repos
        mock_collab_repos.return_value = [repo_obj_mock, repo_obj_mock]

        mock_list_collabs = mock_manager_return.list_collaborators
        mock_list_collabs.return_value = ['collabs']

        response = self.serializer.all_collab_repos()

        expected_response = {
            'repos':
            [{'owner': 'repo_base', 'href': 'mock_url',
              'repo_name': 'repo_name'}, {
                'owner': 'repo_base', 'href': 'mock_url',
                'repo_name': 'repo_name'}]}

        self.assertEqual(response, expected_response)
