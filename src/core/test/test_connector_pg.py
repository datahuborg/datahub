from mock import patch
from django.test import TestCase

# from backend.pg import PGBackend


class SchemaListCreateDeleteShare(TestCase):
    def setUp(self):
        self.repo_name = 'test_repo'
        self.mock_execute_sql = self.create_patch(
            'core.db.backend.pg.PGBackend.execute_sql')
        self.mock_execute_sql.return_value = True

    def create_patch(self, name):
        # helper method for creating patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def test_list_schemas(self):
        self.assertEqual(1, 1)
