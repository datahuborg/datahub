from mock import patch

from django.test import TestCase

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

    def test_query_with_no_repo(self):
        mock_paginate_query = self.mock_manager.return_value.paginate_query

        query = "select * from foo.bar"
        self.serializer.execute_query(query)
        self.assertTrue(mock_paginate_query.called)
