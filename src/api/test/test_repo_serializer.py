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


# self.manager = 139930597827152
# self.mock_manager = 139930608555664
# self.mock_manager.create_repo = 139930596321168