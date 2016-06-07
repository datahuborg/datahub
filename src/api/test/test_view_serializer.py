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
        self.mock_manager.base_url = 'base_uri'
        self.mock_reverse = self.create_patch(
            'api.serializer.reverse')
        self.mock_reverse.return_value = ('mock_url')
        self.serializer = ViewSerializer(
            username=self.username, repo_base=self.repo_base)

    def create_patch(self, name):
        # helper method for creating patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def test_create_view(self):
        mock_manager_create_view = self.mock_manager.return_value.create_view
        mock_manager_create_view.return_value = True

        repo = 'repo_name'
        view = 'view_name'
        query = 'SELECT * FROM table_name'

        success = self.serializer.create_view(repo, view, query)

        self.assertTrue(mock_manager_create_view.called)
        self.assertEqual(success, True)

    def test_list_views(self):
        mock_manager_list_views = self.mock_manager.return_value.list_views
        mock_manager_list_views.return_value = ['view1', 'view2']

        repo = 'repo_name'
        expected_return = {'views': [
                {'view_name': 'view1',
                 'href': 'mock_url'},
                {'view_name': 'view2',
                 'href': 'mock_url'}
            ]}

        views = self.serializer.list_views(repo)

        self.assertTrue(mock_manager_list_views.called)
        self.assertEqual(views, expected_return)

    def test_describe_view_no_detail(self):
        mock_mngr_desc_view = self.mock_manager.return_value.describe_view
        mock_mngr_desc_view.return_value = [(u'id', u'integer'),
                                            (u'words', u'text')]
        repo = 'repo_name'
        view = 'view_name'
        expected_description = {'columns': [
                {"data_type": "integer", "column_name": "id"},
                {"data_type": "text", "column_name": "words"}]
            }
        description = self.serializer.describe_view(repo, view)

        self.assertTrue(mock_mngr_desc_view.called)
        self.assertEqual(description, expected_description)

    def test_delete_view(self):
        mock_manager_delete_view = self.mock_manager.return_value.delete_view
        mock_manager_delete_view.return_value = True

        repo = 'repo_name'
        view = 'view_name'
        success = self.serializer.delete_view(repo, view, False)

        self.assertTrue(mock_manager_delete_view.called)
        self.assertEqual(success, True)

    def test_export_view(self):
        self.serializer.export_view('repo', 'view')
        self.assertTrue(self.mock_manager.return_value.export_view.called)
