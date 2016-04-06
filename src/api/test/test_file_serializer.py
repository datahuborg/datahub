from mock import patch

from django.test import TestCase

from ..serializer import FileSerializer


class FileSerializerTests(TestCase):
    """Test RepoSerializer methods"""

    def setUp(self):
        self.username = "delete_me_username"
        self.repo_base = "delete_me_repo_base"
        self.password = "delete_me_password"

        self.mock_manager = self.create_patch(
            'api.serializer.DataHubManager')
        self.serializer = FileSerializer(
            username=self.username, repo_base=self.repo_base)

    def create_patch(self, name):
        # helper method for creating patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def test_list_files(self):
        mock_list_files = self.mock_manager.return_value.list_repo_files
        self.serializer.list_files('repo')
        self.assertTrue(mock_list_files.called)

    def test_upload_file(self):
        mock_manager_save_file = self.mock_manager.return_value.save_file
        self.serializer.upload_file('repo', 'file')
        self.assertTrue(mock_manager_save_file.called)

    def test_delete_file(self):
        mock_manager_delete_file = self.mock_manager.return_value.delete_file
        self.serializer.delete_file('repo', 'file')
        self.assertTrue(mock_manager_delete_file.called)

    def test_get_file(self):
        mock_manager_get_file = self.mock_manager.return_value.get_file
        self.serializer.get_file('repo', 'file')
        self.assertTrue(mock_manager_get_file.called)
