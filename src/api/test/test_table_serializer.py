from mock import patch

from django.test import TestCase

from ..serializer import TableSerializer


class TableSerializerTests(TestCase):
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
        self.serializer = TableSerializer(
            username=self.username, repo_base=self.repo_base)

    def create_patch(self, name):
        # helper method for creating patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def test_create_table(self):
        mock_manager_create_table = self.mock_manager.return_value.create_table
        mock_manager_create_table.return_value = True

        table = 'table_name'
        repo = 'repo_name'
        params = [
            {'column_name': 'id', 'data_type': 'integer'},
            {'column_name': 'words', 'data_type': 'text'}
        ]

        success = self.serializer.create_table(repo, table, params)

        self.assertTrue(mock_manager_create_table.called)
        self.assertEqual(success, True)

    def test_list_tables(self):
        mock_manager_list_tables = self.mock_manager.return_value.list_tables
        mock_manager_list_tables.return_value = ['table1', 'table2']

        repo = 'repo_name'

        tables = self.serializer.list_tables(repo)
        expected_result = {
            'tables':
            [{'href': 'mock_url', 'table_name': 'table1'},
                {'href': 'mock_url', 'table_name': 'table2'}]
        }

        self.assertTrue(mock_manager_list_tables.called)
        self.assertEqual(tables, expected_result)

    def test_describe_table_no_detail(self):
        mock_mngr_desc_table = self.mock_manager.return_value.describe_table
        mock_mngr_desc_table.return_value = [(u'id', u'integer'),
                                             (u'words', u'text')]
        repo = 'repo_name'
        table = 'table_name'
        expected_description = {
            'columns': [{'data_type': u'integer', 'column_name': u'id'},
                        {'data_type': u'text', 'column_name': u'words'}],
            'permissions': []}
        description = self.serializer.describe_table(repo, table)

        self.assertTrue(mock_mngr_desc_table.called)
        self.assertEqual(description, expected_description)

    def test_delete_table(self):
        mock_manager_delete_table = self.mock_manager.return_value.delete_table
        mock_manager_delete_table.return_value = True

        repo = 'repo_name'
        table = 'table_name'
        success = self.serializer.delete_table(repo, table, False)

        self.assertTrue(mock_manager_delete_table.called)
        self.assertEqual(success, True)

    def test_export_table(self):
        self.serializer.export_table('repo', 'table')
        self.assertTrue(self.mock_manager.return_value.export_table.called)
