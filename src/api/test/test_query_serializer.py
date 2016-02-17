from mock import patch, MagicMock

from django.test import TestCase

from psycopg2 import ProgrammingError
from ..serializer import QuerySerializer


class QuerySerializerTests(TestCase):
    """Test QuerySerializer methods"""

    def setUp(self):
        self.username = "delete_me_username"
        self.repo_base = "delete_me_repo_base"
        self.password = "delete_me_password"

        self.mock_manager = self.create_patch(
            'api.serializer.DataHubManager')
        self.serializer = QuerySerializer(
            username=self.username, repo_base=self.repo_base)

    def create_patch(self, name):
        # helper method for creating patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def test_query_with_no_repo_happy_path(self):
        mock_manager_execute_sql = self.mock_manager.return_value.execute_sql

        query = "select * from foo.bar"
        success, response = self.serializer.execute_sql(query)
        self.assertTrue(mock_manager_execute_sql.called)
        self.assertTrue(success)

    def test_query_with_no_repo_sad_path(self):
        mock_manager_execute_sql = self.mock_manager.return_value.execute_sql
        mock_manager_execute_sql.side_effect = ProgrammingError

        query = "select * from foo.bar"
        success, response = self.serializer.execute_sql(query)

        self.assertTrue(mock_manager_execute_sql.called)

        self.assertFalse(success)
