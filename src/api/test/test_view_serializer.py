from mock import patch

from django.test import TestCase

from ..serializer import ViewSerializer


class ViewSerializerTests(TestCase):
    """Test RepoSerializer methods"""

    def setUp(self):
        self.username = "delete_me_username"
        self.repo_base = "delete_me_repo_base"
        self.password = "delete_me_password"

        self.mock_manager = self.create_patch(
            'api.serializer.DataHubManager')
        self.serializer = ViewSerializer(
            username=self.username, repo_base=self.repo_base)

    def create_patch(self, name):
        # helper method for creating patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def test_export_view(self):
        self.serializer.export_view('repo', 'view')
        self.assertTrue(self.mock_manager.export_view.called)
