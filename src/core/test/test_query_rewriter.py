from core.db.query_rewriter import SQLQueryRewriter

from django.db.models import signals
from django.test import TestCase

import factory
import sqlparse
from mock import patch


class QueryRewriter(TestCase):

    """Tests all the query rewriter operations in query_rewriter.py."""

    @factory.django.mute_signals(signals.pre_save)
    def setUp(self):
        self.repo_base = "test_repobase"
        self.user = "test_user"
        self.query_rewriter = SQLQueryRewriter(self.repo_base, self.user)

        self.mock_connection = self.create_patch(
            'core.db.manager.DataHubConnection')

    def create_patch(self, name):
        # helper method for creating patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def test_extract_table_info(self):
        valid_table_token = "repo.table"
        expected_result = ["repo", "table", None]
        self.assertEqual(
            self.query_rewriter.extract_table_info(valid_table_token),
            expected_result)

        valid_table_token = "repobase.repo.table"
        expected_result = ["repo", "table", "repobase"]
        self.assertEqual(
            self.query_rewriter.extract_table_info(valid_table_token),
            expected_result)

        invalid_table_token = "testtable"
        exception_raised = False
        try:
            self.query_rewriter.extract_table_info(invalid_table_token)
        except Exception:
            exception_raised = True
        self.assertEquals(exception_raised, True)

        invalid_table_token = "table1.table2.table3.table4"
        exception_raised = False
        try:
            self.query_rewriter.extract_table_info(invalid_table_token)
        except Exception:
            exception_raised = True
        self.assertEquals(exception_raised, True)

    def test_extract_table_token(self):
        query = "SELECT * from repo1.table1 as tbl1"
        token = sqlparse.parse(query)[0].tokens[6]
        expected_result = [(["repo1", "table1", None], "as tbl1")]
        self.assertEqual(
            self.query_rewriter.extract_table_token(token), expected_result)

        query = ("SELECT * from repo1.table1 as tbl1, repo2.table2 as tbl2 "
                 "where ... ")
        token = sqlparse.parse(query)[0].tokens[6]
        expected_result = [(["repo1", "table1", None], "as tbl1"),
                           (["repo2", "table2", None], "as tbl2")]
        self.assertEqual(
            self.query_rewriter.extract_table_token(token), expected_result)

        query = "SELECT * from repo1.table1 tbl1, repo2.table2 tbl2 where ... "
        token = sqlparse.parse(query)[0].tokens[6]
        expected_result = [(["repo1", "table1", None], "tbl1"),
                           (["repo2", "table2", None], "tbl2")]
        self.assertEqual(
            self.query_rewriter.extract_table_token(token), expected_result)

    def test_extract_table_string(self):
        valid_table_string = "repo.table"
        expected_result = (["repo", "table", None], '')
        self.assertEqual(
            self.query_rewriter.extract_table_string(valid_table_string),
            expected_result)

        valid_table_string = "repo.table test"
        expected_result = (["repo", "table", None], 'test')
        self.assertEqual(
            self.query_rewriter.extract_table_string(valid_table_string),
            expected_result)

        valid_table_string = "repo.table as test"
        expected_result = (["repo", "table", None], 'as test')
        self.assertEqual(
            self.query_rewriter.extract_table_string(valid_table_string),
            expected_result)

        valid_table_string = "repobase.repo.table test "
        expected_result = (["repo", "table", "repobase"], 'test')
        self.assertEqual(
            self.query_rewriter.extract_table_string(valid_table_string),
            expected_result)

        valid_table_string = "repobase.repo.table as test "
        expected_result = (["repo", "table", "repobase"], 'as test')
        self.assertEqual(
            self.query_rewriter.extract_table_string(valid_table_string),
            expected_result)

        invalid_table_string = "invalidtable"
        exception_raised = False
        try:
            self.query_rewriter.extract_table_string(invalid_table_string)
        except Exception:
            exception_raised = True
        self.assertEquals(exception_raised, True)

    def test_contains_subquery(self):
        query = ("select * from (select * from repo.table where "
                 "repo.table.test = 'True')")
        subquery_token = sqlparse.parse(query)[0].tokens[6]
        no_subquery_token = sqlparse.parse(query)[0].tokens[0]
        self.assertEqual(
            self.query_rewriter.contains_subquery(subquery_token), True)
        self.assertEqual(
            self.query_rewriter.contains_subquery(no_subquery_token), False)

    def test_extract_subquery(self):
        query = ("select * from (select * from repo.table where "
                 "repo.table.test='True')")
        subquery_token = sqlparse.parse(query)[0].tokens[6]
        expected_result = ('(', ('select * from repo.table where '
                                 'repo.table.test=\'True\''), ')')
        self.assertEqual(
            self.query_rewriter.extract_subquery(subquery_token),
            expected_result)

    def test_process_subquery(self):
        query = "select * from (select * from repo.table)"
        subquery_token = sqlparse.parse(query)[0].tokens[6]
        mock_table_policies = self.create_patch(
            'core.db.query_rewriter.SQLQueryRewriter.find_table_policies')
        mock_table_policies.return_value = ["tester='Alice"]
        expected_result = ("(select * from (SELECT * FROM repo.table WHERE "
                           "tester='Alice) AS repotable)")
        self.assertEqual(
            self.query_rewriter.process_subquery(subquery_token),
            expected_result)

    def test_apply_row_level_security_base(self):
        mock_find_table_policies = self.create_patch(
            'core.db.query_rewriter.SQLQueryRewriter.find_table_policies')
        mock_find_table_policies.return_value = ["tester='Alice'"]

        query = "select * from repo.table"
        expected_result = ("select * from (SELECT * FROM repo.table WHERE "
                           "tester='Alice') AS repotable")
        self.assertEqual(
            self.query_rewriter.apply_row_level_security_base(query),
            expected_result)

        query = "select * from hola.orders limit 3"
        expected_result = ("select * from (SELECT * FROM hola.orders WHERE "
                           "tester='Alice') AS holaorders limit 3")
        self.assertEqual(
            self.query_rewriter.apply_row_level_security_base(query),
            expected_result)

        mock_find_table_policies = self.create_patch(
            'core.db.query_rewriter.SQLQueryRewriter.find_table_policies')
        mock_find_table_policies.return_value = ["tester='Alice'",
                                                 "tester='Bob'"]

        query = ("select * from hola.orders o, hola.customer t where "
                 "o.customerid=t.customerid order by customer")
        expected_result = ("select * from (SELECT * FROM hola.orders "
                           "WHERE tester='Alice' OR tester='Bob') o, "
                           "(SELECT * FROM hola.customer WHERE tester='Alice' "
                           "OR tester='Bob') t where o.customerid=t.customerid"
                           " order by customer")
        self.assertEqual(
            self.query_rewriter.apply_row_level_security_base(query),
            expected_result)

        query = ("select * from test.orders right join test.customer "
                 "on test.orders.customerid=test.customer.customerid")
        expected_result = ("select * from (SELECT * FROM test.orders WHERE "
                           "tester='Alice' OR tester='Bob') AS testorders "
                           "right join (SELECT * FROM test.customer WHERE "
                           "tester='Alice' OR tester='Bob') AS testcustomer "
                           "on testorders.customerid=testcustomer.customerid")
        self.assertEqual(
            self.query_rewriter.apply_row_level_security_base(query),
            expected_result)

        query = ("select * from test.orders right join test.customer on "
                 "test.orders.customerid=test.customer.customerid")
        expected_result = ("select * from (SELECT * FROM test.orders WHERE "
                           "tester='Alice' OR tester='Bob') AS testorders "
                           "right join (SELECT * FROM test.customer WHERE "
                           "tester='Alice' OR tester='Bob') AS testcustomer "
                           "on testorders.customerid=testcustomer.customerid")
        self.assertEqual(
            self.query_rewriter.apply_row_level_security_base(query),
            expected_result)

        query = ("select * from test.orders right join test.customer on "
                 "test.orders.customerid=test.customer.customerid")
        expected_result = ("select * from (SELECT * FROM test.orders WHERE "
                           "tester='Alice' OR tester='Bob') AS testorders "
                           "right join (SELECT * FROM test.customer WHERE "
                           "tester='Alice' OR tester='Bob') AS testcustomer "
                           "on testorders.customerid=testcustomer.customerid")
        self.assertEqual(
            self.query_rewriter.apply_row_level_security_base(query),
            expected_result)

        query = "select * from test.orders where test.orders.customerid='1'"
        expected_result = ("select * from (SELECT * FROM test.orders WHERE "
                           "tester='Alice' OR tester='Bob') AS testorders "
                           "where testorders.customerid='1'")
        self.assertEqual(
            self.query_rewriter.apply_row_level_security_base(query),
            expected_result)

        query = ("select count(*), visible from hola.grades_file "
                 "group by visible")
        expected_result = ("select count(*), visible from (SELECT * FROM "
                           "hola.grades_file WHERE tester='Alice' OR "
                           "tester='Bob') AS holagrades_file group by visible")
        self.assertEqual(
            self.query_rewriter.apply_row_level_security_base(query),
            expected_result)

        query = ("select * from (select * from "
                 "(select * from hola.orders) as i) as o")
        expected_result = ("select * from (select * from (select * from "
                           "(SELECT * FROM hola.orders WHERE tester='Alice' "
                           "OR tester='Bob') AS holaorders) as i) as o")
        self.assertEqual(
            self.query_rewriter.apply_row_level_security_base(query),
            expected_result)

        query = ("select * from hola.orders where customerid = "
                 "(select customerid from hola.customer where customerid='3')")
        expected_result = ("select * from (SELECT * FROM hola.orders WHERE "
                           "tester='Alice' OR tester='Bob') AS holaorders "
                           "where customerid = (select customerid from "
                           "(SELECT * FROM hola.customer WHERE tester='Alice' "
                           "OR tester='Bob') AS holacustomer where "
                           "customerid='3')")
        self.assertEqual(
            self.query_rewriter.apply_row_level_security_base(query),
            expected_result)

        query = ("select * from hola.orders as t, hola.orders_2, "
                 "hola.customer where t.customerid=hola.orders_2.customerid "
                 "and hola.orders_2.customerid=hola.customer.customerid")
        expected_result = ("select * from (SELECT * FROM hola.orders WHERE "
                           "tester='Alice' OR tester='Bob') as t, "
                           "(SELECT * FROM hola.orders_2 WHERE tester='Alice' "
                           "OR tester='Bob') AS holaorders_2, "
                           "(SELECT * FROM hola.customer WHERE tester='Alice' "
                           "OR tester='Bob') AS holacustomer where "
                           "t.customerid=holaorders_2.customerid and "
                           "holaorders_2.customerid=holacustomer.customerid")
        self.assertEqual(
            self.query_rewriter.apply_row_level_security_base(query),
            expected_result)

    def test_apply_row_level_security_update(self):
        mock_find_table_policies = self.create_patch(
            'core.db.query_rewriter.SQLQueryRewriter.find_table_policies')
        mock_find_table_policies.return_value = ["count > 10"]
        query = ("update hola.grades_file set firstname='Alice' "
                 "where lastname='Abby'")
        expected_result = ("update hola.grades_file set firstname='Alice' "
                           "where lastname='Abby' AND count > 10")
        self.assertEquals(
            self.query_rewriter.apply_row_level_security_update(query),
            expected_result)

        mock_find_table_policies = self.create_patch(
            'core.db.query_rewriter.SQLQueryRewriter.find_table_policies')
        mock_find_table_policies.return_value = []
        query = ("update hola.grades_file set firstname='Alice' "
                 "where lastname='Abby'")
        expected_result = ("update hola.grades_file set firstname='Alice' "
                           "where lastname='Abby'")
        self.assertEquals(
            self.query_rewriter.apply_row_level_security_update(query),
            expected_result)

    def test_apply_row_level_security_insert(self):
        query = "insert into repo.table values (a,b,c)"
        mock_find_table_policies = self.create_patch(
            'core.db.query_rewriter.SQLQueryRewriter.find_table_policies')
        mock_find_table_policies.return_value = ["INSERT='True'"]
        expected_result = "insert into repo.table values (a,b,c)"
        self.assertEquals(
            self.query_rewriter.apply_row_level_security_insert(query),
            expected_result)

        mock_find_table_policies = self.create_patch(
            'core.db.query_rewriter.SQLQueryRewriter.find_table_policies')
        mock_find_table_policies.return_value = ["INSERT='False'"]

        exception_raised = False
        try:
            self.query_rewriter.apply_row_level_security_insert(query)
        except Exception:
            exception_raised = True
        self.assertEquals(exception_raised, True)

        mock_find_table_policies = self.create_patch(
            'core.db.query_rewriter.SQLQueryRewriter.find_table_policies')
        mock_find_table_policies.return_value = []
        self.assertEquals(
            self.query_rewriter.apply_row_level_security_insert(query),
            expected_result)

    def test_apply_row_level_security(self):
        mock_apply_rls_base = self.create_patch(
            'core.db.query_rewriter.SQLQueryRewriter.'
            'apply_row_level_security_base')
        mock_apply_rls_base.return_value = "RLS for select called"

        mock_apply_rls_insert = self.create_patch(
            'core.db.query_rewriter.SQLQueryRewriter.'
            'apply_row_level_security_insert')
        mock_apply_rls_insert.return_value = "RLS for insert called"

        mock_apply_rls_update = self.create_patch(
            'core.db.query_rewriter.SQLQueryRewriter.'
            'apply_row_level_security_update')
        mock_apply_rls_update.return_value = "RLS for update called"

        select_query = "select * from repo.table"
        self.assertEquals(
            self.query_rewriter.apply_row_level_security(select_query),
            "RLS for select called")

        insert_query = "insert into repo.table values (a,b,c)"
        self.assertEquals(
            self.query_rewriter.apply_row_level_security(insert_query),
            "RLS for insert called")

        update_query = ("update repo.table set firstname='Alice' "
                        "where lastname='Abby'")
        self.assertEquals(
            self.query_rewriter.apply_row_level_security(update_query),
            "RLS for update called")
