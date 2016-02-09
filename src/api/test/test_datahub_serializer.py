from mock import patch

from django.test import TestCase

from ..serializer import DataHubSerializer


class DataHubSerializerTests(TestCase):
    """Test DataHubSerializer methods"""

    def setUp(self):
        self.username = "delete_me_username"
        self.repo_base = "delete_me_repo_base"
        self.password = "delete_me_password"

        self.mock_manager = self.create_patch(
            'api.serializer.DataHubManager')
        self.serializer = DataHubSerializer(
            username=self.username, repo_base=self.repo_base)

    def create_patch(self, name):
        # helper method for creating patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def test_initialization(self):
        dataHubSerializer = DataHubSerializer(
            username=self.username, repo_base=self.repo_base)

        self.assertEqual(dataHubSerializer.username, self.username)
        self.assertEqual(dataHubSerializer.repo_base, self.repo_base)
        self.assertEqual(
            self.mock_manager.call_args[1]['repo_base'], self.repo_base)
        self.assertEqual(
            self.mock_manager.call_args[1]['user'], self.username)
