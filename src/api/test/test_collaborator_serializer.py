from mock import patch

from django.test import TestCase

from ..serializer import CollaboratorSerializer


class CollaboratorSerializerTests(TestCase):
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
        self.serializer = CollaboratorSerializer(
            username=self.username, repo_base=self.repo_base)

    def create_patch(self, name):
        # helper method for creating patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def test_list_collaborators(self):
        list_collab_result = [
                {'username': 'collab1', 'privileges': 'UC'},
                {'username': 'collab2', 'privileges': 'U'}]

        mock_list_collabs = self.mock_manager.return_value.list_collaborators
        mock_list_collabs.return_value = list_collab_result

        expected_result = {'collaborators': [
                        {'username': 'collab1', 'href': 'mock_url'},
                        {'username': 'collab2', 'href': 'mock_url'}]}

        res = self.serializer.list_collaborators('repo_name')
        self.assertEqual(expected_result, res)

    def test_add_collaborator(self):
        mock_add_collab = self.mock_manager.return_value.add_collaborator
        mock_add_collab.return_value = True

        res = self.serializer.add_collaborator('repo_name', 'collab', [], [])
        self.assertTrue(mock_add_collab.called)
        self.assertEqual(True, res)

    def test_remove_collaborator(self):
        mock_remove_collab = self.mock_manager.return_value.delete_collaborator
        mock_remove_collab.return_value = True

        res = self.serializer.remove_collaborator('repo_name', 'collab')
        self.assertTrue(mock_remove_collab.called)
        self.assertEqual(True, res)
