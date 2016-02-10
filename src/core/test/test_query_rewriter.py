from core.db.manager import DataHubManager
from core.db.query_rewriter import SQLQueryRewriter

from django.db.models import signals
from django.contrib.auth.models import User
from django.test import TestCase

import factory
import sqlparse
from mock import patch


class Initialization(TestCase):

    """Test the correct user is returned."""

    @factory.django.mute_signals(signals.pre_save)
    def setUp(self):
        self.username = "test_username"
        self.password = "_test diff1;cul t passw0rd-"
        self.email = "test_email@csail.mit.edu"
        self.user = User.objects.create_user(
            self.username, self.email, self.password)

        self.mock_connection = self.create_patch(
            'core.db.manager.DataHubConnection')

    def create_patch(self, name):
        # helper method for creating patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def test_initialization(self):
        DataHubManager(user=self.username)

        # username passed
        self.assertEqual(
            self.mock_connection.call_args[1]['user'], self.username)

        # password passed
        self.assertTrue(
            self.mock_connection.call_args[1]['password'] is not None)

        # repo defaults to username
        self.assertEqual(
            self.mock_connection.call_args[1]['repo_base'], self.username)


class QueryRewriter(TestCase):

    """Tests all the query rewriter operations in query_rewriter.py."""

    @factory.django.mute_signals(signals.pre_save)
    def setUp(self):
        self.username = "test_username"
        self.password = "_test diff1;cul t passw0rd-"
        self.email = "test_email@csail.mit.edu"
        self.user = User.objects.create_user(
            self.username, self.email, self.password)

        self.mock_connection = self.create_patch(
            'core.db.manager.DataHubConnection')

        self.manager = DataHubManager(user=self.username)


        self.query1 = "SELECT * FROM repo1.Orders INNER JOIN (select col1 from repo2.Customers) ON Orders.CustomerID=Customers.CustomerID;"
        self.query1_tokens = sqlparse.parse(self.query1)[0].tokens

        self.query2 = "SELECT * FROM repo1.Orders WHERE id = (SELECT a FROM repo1.table1 JOIN repo2.table1 ON table1.id=table2.id);"
        self.query2_tokens = sqlparse.parse(self.query2)[0].tokens

    
    def create_patch(self, name):
        # helper method for creating patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def test_contain_subquery(self):
        self.assertTrue(SQLQueryRewriter.contain_subquery(self.query1_tokens[5]))
        self.assertFalse(SQLQueryRewriter.contain_subquery(self.query1_tokens[0]))

    def test_process_subquery(self):
        result = "(select col1 from repo2.Customers where repo2=Customers)"
        self.assertEqual(SQLQueryRewriter.process_subquery(self.query1_tokens[5]), result)

    def test_found_join(self):
        self.assertTrue(SQLQueryRewriter.found_join(self.query1_tokens[3]))
        self.assertFalse(SQLQueryRewriter.found_join(self.query1_tokens[0]))
        # Nested queries with join tokens should still return False on outter check
        self.assertFalse(SQLQueryRewriter.found_join(self.query2_tokens[5]))

    def test_extract_table_information(self):
        self.assertEqual(SQLQueryRewriter.extract_table_information(None, self.query1_tokens[3]), ("repo1", "Orders"))
        self.assertEqual(SQLQueryRewriter.extract_table_information(("A", "B"), self.query1_tokens[0]), ("A", "B"))
        self.assertEqual(SQLQueryRewriter.extract_table_information(None, self.query1_tokens[0]), None)

    def test_get_security_policy_string(self):
        #TODO: Write test case for this after security policy table is set up
        pass

    def test_contains_join_subquery(self):
        self.assertTrue(SQLQueryRewriter.contains_join_subquery(self.query2_tokens[5]))
        self.assertFalse(SQLQueryRewriter.contains_join_subquery(self.query1_tokens[5]))

    def test_process_subqueries(self):
        result = "SELECT * FROM repo1.Orders INNER JOIN (select col1 from repo2.Customers WHERE repo2=Customers) ON Orders.CustomerID=Customers.CustomerID;"
        self.assertEqual(SQLQueryRewriter.process_subqueries(self.query1), result)

    def test_process_join_query(self):
        result = "SELECT * FROM (SELECT * FROM repo1.Orders WHERE repo1=Orders) INNER JOIN  (select col1 from repo2.Customers WHERE repo2=Customers) ON Orders.CustomerID=Customers.CustomerID;"
        self.assertEquals(SQLQueryRewriter.process_join_query(self.query1), result)

    def test_transform_table_to_rls_subquery(self):
        result = "(SELECT * from repo1.Orders where repo1=Orders)"
        self.assertEqual(SQLQueryRewriter.transform_table_to_rls_subquery(self.query1_token(3)), result)

    def test_find_security_policy(self):
        #TODO: Write test case after secutiy policy table is set up
        pass


    def test_apply_row_level_security(self):
        query1 = "SELECT * FROM repo1.table1 WHERE id = (SELECT column_name FROM repo2.table2 WHERE id = 2);"
        query2 = "SELECT * from (select x.foo, x.bar as foo2, x.baz from (select * from table1.mytable));" 
        query3 = "SELECT * FROM repo1.Orders INNER JOIN repo2.Customers ON Orders.CustomerID=Customers.CustomerID;"
        query4 = "SELECT * FROM repo.Orders;"
        query5 = "SELECT * FROM (SELECT repo1.column FROM table1 WHERE id = 1) OPERATOR (SELECT column_name FROM repo2.table2 WHERE id = 2);"
        query6 = "SELECT * FROM repo1.Orders INNER JOIN (select col1 from repo2.Customers) ON Orders.CustomerID=Customers.CustomerID;"
        query7 = "SELECT * FROM repo1.Orders WHERE id = (SELECT a FROM repo1.table1 JOIN repo2.table1 ON table1.id=table2.id);"
        query8 = "SELECT * FROM repo1.orders1 JOIN repo2.orders2 WHERE id=5;"
        
        expected_query1 = "SELECT * FROM repo1.table1 WHERE id = (SELECT column_name FROM repo2.table2 WHERE id = 2 AND repo2=table2) AND repo1=table1;"
        expected_query2 = "SELECT * from (select x.foo, x.bar as foo2, x.baz from (select * from table1.mytable WHERE table1=mytable));"
        expected_query3 = "SELECT * FROM (SELECT * FROM repo1.Orders WHERE repo1=Orders) INNER JOIN  (SELECT * FROM repo2.Customers WHERE repo2=Customers) ON Orders.CustomerID=Customers.CustomerID ;"
        expected_query4 = "SELECT * FROM repo.Orders;"
        expected_query5 = "SELECT * FROM (SELECT repo1.column FROM table1 WHERE id = 1 AND repo1=column) OPERATOR (SELECT column_name FROM repo2.table2 WHERE id = 2 AND repo2=table2);"
        expected_query6 = "SELECT * FROM (SELECT * FROM repo1.Orders WHERE repo1=Orders) INNER JOIN  (select col1 from repo2.Customers WHERE repo2=Customers) ON Orders.CustomerID=Customers.CustomerID;"
        expected_query7 = "SELECT * FROM repo1.Orders WHERE id = (SELECT a FROM (SELECT * FROM repo1.table1 WHERE repo1=table1) JOIN  (SELECT * FROM repo2.table1 WHERE repo2=table1) ON table1.id=table2.id ) AND repo1=Orders;"
        expected_query8 = "SELECT * FROM (SELECT * FROM repo1.orders1 WHERE repo1=orders1) JOIN  (SELECT * FROM repo2.orders2 WHERE repo2=orders2) WHERE id=5;"

        self.assertEqual(SQLQueryRewriter.apply_row_level_security(query1), expected_query1)
        self.assertEqual(SQLQueryRewriter.apply_row_level_security(query2), expected_query2)
        self.assertEqual(SQLQueryRewriter.apply_row_level_security(query3), expected_query3)
        self.assertEqual(SQLQueryRewriter.apply_row_level_security(query4), expected_query4)
        self.assertEqual(SQLQueryRewriter.apply_row_level_security(query5), expected_query5)
        self.assertEqual(SQLQueryRewriter.apply_row_level_security(query6), expected_query6)
        self.assertEqual(SQLQueryRewriter.apply_row_level_security(query7), expected_query7)
        self.assertEqual(SQLQueryRewriter.apply_row_level_security(query8), expected_query8)



     








