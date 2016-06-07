from mock import Mock, \
                 MagicMock, \
                 patch, \
                 mock_open
import itertools

from django.test import TestCase

from config.settings import PUBLIC_ROLE
from core.db.backend.pg import connection_pools, \
                               _pool_for_credentials, \
                               PGBackend


class MockingMixin(object):
    """A mixin for mock helper methods"""

    def create_patch(self, name, **kwargs):
        """
        Returns a started patch which stops itself on test cleanup.

        Any kwargs pass directly into patch().
        """
        patcher = patch(name, **kwargs)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing


class PoolHelperFunctions(MockingMixin, TestCase):
    """Tests helper functions in pg.py, but not in the PGBackend class."""

    def setUp(self):
        self.mock_ThreadedConnectionPool = self.create_patch(
            'core.db.backend.pg.ThreadedConnectionPool')

    def test_pool_for_credentials(self):
        n = len(connection_pools)
        _pool_for_credentials('foo', 'password', 'repo_base')
        self.assertEqual(len(connection_pools), n + 1)
        _pool_for_credentials('bar', 'password', 'repo_base',
                              create_if_missing=True)
        self.assertEqual(len(connection_pools), n + 2)
        _pool_for_credentials('baz', 'password', 'repo_base',
                              create_if_missing=False)
        self.assertEqual(len(connection_pools), n + 2)
        _pool_for_credentials('bar', 'wordpass', 'repo_base')
        self.assertEqual(len(connection_pools), n + 3)

    # psycopg2 doesn't expose any good way to test that close_all_connections
    # works. You can't ask for the list of existing connections and check that
    # they're closed.
    # def test_close_all_connections(self):


class PGBackendHelperMethods(MockingMixin, TestCase):
    """Tests connections, validation and execution methods in PGBackend."""

    def setUp(self):
        # some words to test out
        self.good_nouns = ['good', 'good_noun', 'goodNoun', 'good1']

        # some words that should throw validation errors
        self.bad_nouns = ['_foo', 'foo_', '-foo', 'foo-', 'foo bar', '1foo',
                          'injection;attack', ';injection', 'injection;',
                          ]

        self.username = "username"
        self.password = "password"

        # mock connection pools so nothing gets a real db connection
        self.mock_pool_for_cred = self.create_patch(
            'core.db.backend.pg._pool_for_credentials')

        # mock open connection, only to check if it ever gets called directly
        self.mock_connect = self.create_patch(
            'core.db.backend.pg.psycopg2.connect')

        # open mocked connection
        self.backend = PGBackend(self.username,
                                 self.password,
                                 repo_base=self.username)

    def tearDown(self):
        # Make sure connections are only ever acquired via pools
        self.assertFalse(self.mock_connect.called)

    def test_check_for_injections(self):
        """Tests validation against some sql injection attacks."""
        for noun in self.bad_nouns:
            with self.assertRaises(ValueError):
                self.backend._check_for_injections(noun)

        for noun in self.good_nouns:
            try:
                self.backend._check_for_injections(noun)
            except ValueError:
                self.fail('_check_for_injections failed to verify a good name')

    def test_validate_table_names(self):
        """Tests validation against some invalid table names."""
        good_tables = ['table', '_dbwipes_cache', 'my_repo1',
                       'asdfl_fsdvbrbhg_______jkhadsc']
        bad_tables = [' table', '1table', 'table;select * from somewhere',
                      'table-table']
        for noun in bad_tables:
            with self.assertRaises(ValueError):
                self.backend._validate_table_name(noun)

        for noun in good_tables:
            try:
                self.backend._validate_table_name(noun)
            except ValueError:
                self.fail('_validate_table_name failed to verify a good name')

    def test_check_open_connections(self):
        mock_get_conn = self.mock_pool_for_cred.return_value.getconn
        mock_set_isol_level = mock_get_conn.return_value.set_isolation_level

        self.assertTrue(self.mock_pool_for_cred.called)
        self.assertTrue(mock_get_conn.called)
        self.assertTrue(mock_set_isol_level.called)

    def test_execute_sql_strips_queries(self):
        query = ' This query needs stripping; '
        params = ('param1', 'param2')

        mock_cursor = self.backend.connection.cursor
        mock_execute = mock_cursor.return_value.execute
        mock_cursor.return_value.fetchall.return_value = 'sometuples'
        mock_cursor.return_value.rowcount = 1000

        mock_query_rewriter = MagicMock()
        mock_query_rewriter.apply_row_level_security.side_effect = lambda x: x
        self.backend.query_rewriter = mock_query_rewriter

        res = self.backend.execute_sql(query, params)

        self.assertTrue(mock_query_rewriter.apply_row_level_security.called)
        self.assertTrue(mock_cursor.called)
        self.assertTrue(mock_execute.called)

        self.assertEqual(res['tuples'], 'sometuples')
        self.assertEqual(res['status'], True)
        self.assertEqual(res['row_count'], 1000)


class SchemaListCreateDeleteShare(MockingMixin, TestCase):
    """
    Tests that items reach the execute_sql method in pg.py.

    Does not test execute_sql itself.
    """

    def setUp(self):
        # some words to test out
        self.good_nouns = ['good', 'good_noun', 'good-noun']
        # some words that shoudl throw validation errors
        self.bad_nouns = ['_foo', 'foo_', '-foo', 'foo-', 'foo bar',
                          'injection;attack', ';injection', 'injection;',
                          ]

        self.username = "username"
        self.password = "p4 sS_W&*^;0Rd$_"

        # mock the execute_sql function
        self.mock_execute_sql = self.create_patch(
            'core.db.backend.pg.PGBackend.execute_sql')
        self.mock_execute_sql.return_value = True

        # mock the mock_check_for_injections, which checks for injection
        # attacks
        self.mock_check_for_injections = self.create_patch(
            'core.db.backend.pg.PGBackend._check_for_injections')

        self.mock_validate_table_name = self.create_patch(
            'core.db.backend.pg.PGBackend._validate_table_name')

        # mock open connection, or else it will try to
        # create a real db connection
        self.mock_open_connection = self.create_patch(
            'core.db.backend.pg.PGBackend.__open_connection__')

        # mock the psycopg2.extensions.AsIs - many of the pg.py methods use it
        # Its return value (side effect) is the call value
        self.mock_as_is = self.create_patch('core.db.backend.pg.AsIs')
        self.mock_as_is.side_effect = lambda x: x

        # create an instance of PGBackend
        self.backend = PGBackend(self.username,
                                 self.password,
                                 repo_base=self.username)

    def reset_mocks(self):
        # clears the mock call arguments and sets their call counts to 0
        self.mock_as_is.reset_mock()
        self.mock_execute_sql.reset_mock()
        self.mock_check_for_injections.reset_mock()

    # testing externally called methods in PGBackend
    def test_create_repo(self):
        create_repo_sql = 'CREATE SCHEMA IF NOT EXISTS %s AUTHORIZATION %s'
        reponame = 'reponame'
        self.mock_execute_sql.return_value = {'status': True, 'row_count': -1,
                                              'tuples': [], 'fields': []}

        res = self.backend.create_repo(reponame)
        self.assertEqual(
            self.mock_execute_sql.call_args[0][0], create_repo_sql)
        self.assertEqual(
            self.mock_execute_sql.call_args[0][1][0], reponame)
        self.assertEqual(
            self.mock_execute_sql.call_args[0][1][1], self.username)

        self.assertTrue(self.mock_as_is.called)
        self.assertTrue(self.mock_check_for_injections.called)
        self.assertEqual(res, True)

    def test_list_repos(self):
        # the user is already logged in, so there's not much to be tested here
        # except that the arguments are passed correctly
        list_repo_sql = ('SELECT schema_name AS repo_name '
                         'FROM information_schema.schemata '
                         'WHERE schema_owner != %s')

        mock_settings = self.create_patch("core.db.backend.pg.settings")
        mock_settings.DATABASES = {'default': {'USER': 'postgres'}}

        self.mock_execute_sql.return_value = {
            'status': True, 'row_count': 1, 'tuples': [
                ('test_table',)],
            'fields': [{'type': 1043, 'name': 'table_name'}]}

        params = (mock_settings.DATABASES['default']['USER'],)
        res = self.backend.list_repos()
        self.assertEqual(
            self.mock_execute_sql.call_args[0][0], list_repo_sql)
        self.assertEqual(
            self.mock_execute_sql.call_args[0][1], params)

        self.assertEqual(res, ['test_table'])

    def test_rename_repo(self):
        alter_repo_sql = 'ALTER SCHEMA %s RENAME TO %s'
        self.mock_execute_sql.return_value = {
            'status': True, 'row_count': 1, 'tuples': [
                ('test_table',)],
            'fields': [{'type': 1043, 'name': 'table_name'}]}

        params = ('old_name', 'new_name')

        res = self.backend.rename_repo('old_name', 'new_name')
        self.assertEqual(res, True)
        self.assertEqual(
            self.mock_execute_sql.call_args[0][0], alter_repo_sql)
        self.assertEqual(
            self.mock_execute_sql.call_args[0][1], params)

        self.assertTrue(self.mock_execute_sql.called)
        self.assertEqual(self.mock_check_for_injections.call_count, 2)

    def test_delete_repo_happy_path_cascade(self):
        drop_schema_sql = 'DROP SCHEMA %s %s'
        repo_name = 'repo_name'
        self.mock_execute_sql.return_value = {'status': True, 'row_count': -1,
                                              'tuples': [], 'fields': []}

        res = self.backend.delete_repo(repo=repo_name, force=True)
        self.assertEqual(
            self.mock_execute_sql.call_args[0][0], drop_schema_sql)
        self.assertEqual(
            self.mock_execute_sql.call_args[0][1][0], repo_name)
        self.assertEqual(
            self.mock_execute_sql.call_args[0][1][1], 'CASCADE')
        self.assertTrue(self.mock_as_is.called)
        self.assertTrue(self.mock_check_for_injections)
        self.assertEqual(res, True)

    def test_delete_repo_no_cascade(self):
        drop_schema_sql = 'DROP SCHEMA %s %s'
        repo_name = 'repo_name'
        self.mock_execute_sql.return_value = {'status': True, 'row_count': -1,
                                              'tuples': [], 'fields': []}

        res = self.backend.delete_repo(repo=repo_name, force=False)
        self.assertEqual(
            self.mock_execute_sql.call_args[0][0], drop_schema_sql)
        self.assertEqual(
            self.mock_execute_sql.call_args[0][1][0], repo_name)
        self.assertEqual(
            self.mock_execute_sql.call_args[0][1][1], '')
        self.assertTrue(self.mock_as_is.called)
        self.assertTrue(self.mock_check_for_injections.called)
        self.assertEqual(res, True)

    def test_add_collaborator(self):
        privileges = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'TRUNCATE',
                      'REFERENCES', 'TRIGGER', 'CREATE', 'CONNECT',
                      'TEMPORARY', 'EXECUTE', 'USAGE']

        add_collab_query = ('BEGIN;'
                            'GRANT USAGE ON SCHEMA %s TO %s;'
                            'GRANT %s ON ALL TABLES IN SCHEMA %s TO %s;'
                            'ALTER DEFAULT PRIVILEGES IN SCHEMA %s '
                            'GRANT %s ON TABLES TO %s;'
                            'COMMIT;'
                            )

        self.mock_execute_sql.return_value = {'status': True, 'row_count': -1,
                                              'tuples': [], 'fields': []}

        product = itertools.product(self.good_nouns, self.good_nouns,
                                    privileges)

        # test every combo here. For now, don't test combined privileges

        for repo, receiver, privilege in product:

            params = (repo, receiver, privilege, repo, receiver,
                      repo, privilege, receiver)

            res = self.backend.add_collaborator(
                repo=repo, collaborator=receiver, db_privileges=[privilege])

            self.assertEqual(
                self.mock_execute_sql.call_args[0][0], add_collab_query)
            self.assertEqual(self.mock_execute_sql.call_args[0][1], params)
            self.assertEqual(self.mock_as_is.call_count, len(params))

            self.assertEqual(self.mock_check_for_injections.call_count, 3)
            self.assertEqual(res, True)

            self.reset_mocks()

    def test_add_collaborator_concatenates_privileges(self):
        privileges = ['SELECT', 'USAGE']
        repo = 'repo'
        receiver = 'receiver'
        self.mock_execute_sql.return_value = {'status': True, 'row_count': -1,
                                              'tuples': [], 'fields': []}

        self.backend.add_collaborator(repo=repo,
                                      collaborator=receiver,
                                      db_privileges=privileges)

        # make sure that the privileges are passed as a string in params
        self.assertTrue(
            'SELECT, USAGE' in self.mock_execute_sql.call_args[0][1])

    def test_delete_collaborator(self):
        delete_collab_sql = ('BEGIN;'
                             'REVOKE ALL ON ALL TABLES IN SCHEMA %s '
                             'FROM %s CASCADE;'
                             'REVOKE ALL ON SCHEMA %s FROM %s CASCADE;'
                             'ALTER DEFAULT PRIVILEGES IN SCHEMA %s '
                             'REVOKE ALL ON TABLES FROM %s;'
                             'COMMIT;'
                             )
        self.mock_execute_sql.return_value = {'status': True, 'row_count': -1,
                                              'tuples': [], 'fields': []}

        repo = 'repo_name'
        username = 'delete_me_user_name'

        params = (repo, username, repo, username, repo, username)
        res = self.backend.delete_collaborator(
            repo=repo, collaborator=username)

        self.assertEqual(
            self.mock_execute_sql.call_args[0][0], delete_collab_sql)
        self.assertEqual(self.mock_execute_sql.call_args[0][1], params)
        self.assertEqual(self.mock_as_is.call_count, len(params))
        self.assertEqual(self.mock_check_for_injections.call_count, 2)
        self.assertEqual(res, True)

    def test_create_table(self):
        repo = 'repo'
        table = 'table'
        params = [
            {'column_name': 'id', 'data_type': 'integer'},
            {'column_name': 'words', 'data_type': 'text'}
            ]
        expected_params = ('repo', 'table', 'id integer, words text')

        create_table_query = ('CREATE TABLE %s.%s (%s)')

        self.mock_execute_sql.return_value = {
            'status': True, 'row_count': -1, 'tuples': [], 'fields': []}

        res = self.backend.create_table(repo, table, params)

        # checks repo, table, and all param values for injections
        self.assertEqual(self.mock_check_for_injections.call_count, 5)
        self.assertEqual(self.mock_validate_table_name.call_count, 1)

        final_query = self.mock_execute_sql.call_args[0][0]
        final_params = self.mock_execute_sql.call_args[0][1]
        self.assertEqual(final_query, create_table_query)
        self.assertEqual(final_params, expected_params)
        self.assertEqual(res, True)

        # create table test_repo.test_table (id integer, words text)

    def test_list_tables(self):
        repo = 'repo'
        list_tables_query = ('SELECT table_name FROM '
                             'information_schema.tables '
                             'WHERE table_schema = %s '
                             'AND table_type = \'BASE TABLE\';')
        params = (repo,)

        # execute sql should return this:
        self.mock_execute_sql.return_value = {
            'status': True, 'row_count': 1, 'tuples': [
                ('test_table',)],
            'fields': [{'type': 1043, 'name': 'table_name'}]}

        # mocking out execute_sql's complicated return JSON
        mock_list_repos = self.create_patch(
            'core.db.backend.pg.PGBackend.list_repos')
        mock_list_repos.return_value = [repo]

        res = self.backend.list_tables(repo)
        self.assertEqual(
            self.mock_execute_sql.call_args[0][0], list_tables_query)
        self.assertEqual(self.mock_execute_sql.call_args[0][1], params)
        self.assertEqual(self.mock_check_for_injections.call_count, 1)
        self.assertEqual(res, ['test_table'])

    def test_describe_table_without_detail(self):
        repo = 'repo'
        table = 'table'
        detail = False

        query = ("SELECT %s "
                 "FROM information_schema.columns "
                 "WHERE table_schema = %s and table_name = %s;")
        params = ('column_name, data_type', repo, table)

        self.mock_execute_sql.return_value = {
            'status': True, 'row_count': 2,
            'tuples': [(u'id', u'integer'), (u'words', u'text')],
            'fields': [
                {'type': 1043, 'name': 'column_name'},
                {'type': 1043, 'name': 'data_type'}
                ]
            }

        res = self.backend.describe_table(repo, table, detail)

        self.assertEqual(self.mock_execute_sql.call_args[0][0], query)
        self.assertEqual(self.mock_execute_sql.call_args[0][1], params)
        self.assertEqual(res,  [(u'id', u'integer'), (u'words', u'text')])

    def test_describe_table_query_in_detail(self):
        repo = 'repo'
        table = 'table'
        detail = True

        query = ("SELECT %s "
                 "FROM information_schema.columns "
                 "WHERE table_schema = %s and table_name = %s;")
        params = ('*', repo, table)

        self.mock_execute_sql.return_value = {
            'status': True, 'row_count': 2,
            'tuples': [
                (u'id', u'integer'), (u'words', u'text'), ('foo', 'bar')
                ],
            'fields': [
                {'type': 1043, 'name': 'column_name'},
                {'type': 1043, 'name': 'data_type'}
                ]
            }

        res = self.backend.describe_table(repo, table, detail)

        self.assertEqual(self.mock_execute_sql.call_args[0][0], query)
        self.assertEqual(self.mock_execute_sql.call_args[0][1], params)
        self.assertEqual(
            res,  [(u'id', u'integer'), (u'words', u'text'), ('foo', 'bar')])

    def test_list_table_permissions(self):
        repo = 'repo'
        table = 'table'
        query = ("select privilege_type from "
                 "information_schema.role_table_grants where table_schema=%s "
                 "and table_name=%s and grantee=%s")
        params = ('repo', 'table', self.username)
        self.mock_execute_sql.return_value = {
            'status': True, 'row_count': 2,
            'tuples': [
                (u'SELECT'), (u'UPDATE')],
            'fields': [{'type': 1043, 'name': 'privilege_type'}]
            }

        self.backend.list_table_permissions(repo, table)
        self.assertEqual(self.mock_execute_sql.call_args[0][0], query)
        self.assertEqual(self.mock_execute_sql.call_args[0][1], params)

    def test_delete_table(self):
        repo = 'repo_name'
        table = 'table_name'
        force = False

        expected_query = ('DROP TABLE %s.%s.%s %s')
        expected_params = ('username', 'repo_name', 'table_name', 'RESTRICT')
        self.mock_execute_sql.return_value = {
            'status': True, 'row_count': -1, 'tuples': [], 'fields': []}
        res = self.backend.delete_table(repo, table, force)

        final_query = self.mock_execute_sql.call_args[0][0]
        final_params = self.mock_execute_sql.call_args[0][1]

        self.assertEqual(self.mock_check_for_injections.call_count, 1)
        self.assertEqual(self.mock_validate_table_name.call_count, 1)
        self.assertEqual(final_query, expected_query)
        self.assertEqual(final_params, expected_params)
        self.assertEqual(res, True)

    def test_list_views(self):
        repo = 'repo'
        list_views_query = ('SELECT table_name FROM information_schema.tables '
                            'WHERE table_schema = %s '
                            'AND table_type = \'VIEW\';')
        params = (repo,)

        # mocking out execute_sql's complicated return JSON
        self.mock_execute_sql.return_value = {
            'status': True, 'row_count': 1, 'tuples': [
                ('test_view',)],
            'fields': [{'type': 1043, 'name': 'view_name'}]}

        # list_views depends on list_repos, which is being mocked out
        mock_list_repos = self.create_patch(
            'core.db.backend.pg.PGBackend.list_repos')
        mock_list_repos.return_value = [repo]

        res = self.backend.list_views(repo)
        self.assertEqual(
            self.mock_execute_sql.call_args[0][0], list_views_query)
        self.assertEqual(self.mock_execute_sql.call_args[0][1], params)
        self.assertEqual(self.mock_check_for_injections.call_count, 1)
        self.assertEqual(res, ['test_view'])

    def test_delete_view(self):
        repo = 'repo_name'
        view = 'view_name'
        force = False

        expected_query = ('DROP VIEW %s.%s.%s %s')
        expected_params = ('username', 'repo_name', 'view_name', 'RESTRICT')
        self.mock_execute_sql.return_value = {
            'status': True, 'row_count': -1, 'tuples': [], 'fields': []}
        res = self.backend.delete_view(repo, view, force)

        final_query = self.mock_execute_sql.call_args[0][0]
        final_params = self.mock_execute_sql.call_args[0][1]

        self.assertEqual(self.mock_check_for_injections.call_count, 1)
        self.assertEqual(self.mock_validate_table_name.call_count, 1)
        self.assertEqual(final_query, expected_query)
        self.assertEqual(final_params, expected_params)
        self.assertEqual(res, True)

    def test_create_view(self):
        repo = 'repo_name'
        view = 'view_name'
        sql = 'SELECT * FROM table'

        expected_params = ('repo_name', 'view_name', 'SELECT * FROM table')
        create_view_query = ('CREATE VIEW %s.%s AS (%s)')
        self.mock_execute_sql.return_value = {
            'status': True, 'row_count': -1, 'tuples': [], 'fields': []}
        res = self.backend.create_view(repo, view, sql)

        # checks repo and view for injections
        self.assertEqual(self.mock_check_for_injections.call_count, 1)
        self.assertEqual(self.mock_validate_table_name.call_count, 1)

        final_query = self.mock_execute_sql.call_args[0][0]
        final_params = self.mock_execute_sql.call_args[0][1]
        self.assertEqual(final_query, create_view_query)
        self.assertEqual(final_params, expected_params)
        self.assertEqual(res, True)

    def test_describe_view_without_detail(self):
        repo = 'repo_name'
        view = 'view_name'
        detail = False

        query = ("SELECT %s "
                 "FROM information_schema.columns "
                 "WHERE table_schema = %s and table_name = %s;")
        params = ('column_name, data_type', repo, view)

        self.mock_execute_sql.return_value = {
            'status': True, 'row_count': 2,
            'tuples': [(u'id', u'integer'), (u'words', u'text')],
            'fields': [
                {'type': 1043, 'name': 'column_name'},
                {'type': 1043, 'name': 'data_type'}
                ]
            }

        res = self.backend.describe_view(repo, view, detail)

        self.assertEqual(self.mock_execute_sql.call_args[0][0], query)
        self.assertEqual(self.mock_execute_sql.call_args[0][1], params)
        self.assertEqual(res,  [(u'id', u'integer'), (u'words', u'text')])

    def test_get_schema(self):

        self.mock_execute_sql.return_value = {
            'status': True, 'row_count': 2,
            'tuples': [(u'id', u'integer'), (u'words', u'text')],
            'fields': [
                {'type': 1043, 'name': 'column_name'},
                {'type': 1043, 'name': 'data_type'}
            ]
        }

        repo = 'repo'
        table = 'table'

        get_schema_query = ('SELECT column_name, data_type '
                            'FROM information_schema.columns '
                            'WHERE table_name = %s '
                            'AND table_schema = %s;'
                            )
        params = ('table', 'repo')

        self.backend.get_schema(repo, table)
        self.assertEqual(
            self.mock_execute_sql.call_args[0][0], get_schema_query)
        self.assertEqual(self.mock_execute_sql.call_args[0][1], params)
        self.assertEqual(self.mock_check_for_injections.call_count, 1)
        self.assertEqual(self.mock_validate_table_name.call_count, 1)

    def test_create_public_user_no_create_db(self):
        create_user_query = ('CREATE ROLE %s WITH LOGIN '
                             'NOCREATEDB NOCREATEROLE NOCREATEUSER '
                             'PASSWORD %s')

        username = PUBLIC_ROLE
        password = 'password'

        self.backend.create_user(username, password, create_db=False)
        params = (username, password)
        mock_create_user_database = self.create_patch(
            'core.db.backend.pg.PGBackend.create_user_database')

        # import pdb; pdb.set_trace()
        self.assertEqual(
            self.mock_execute_sql.call_args[0][0], create_user_query)
        self.assertEqual(self.mock_execute_sql.call_args[0][1], params)
        self.assertEqual(self.mock_as_is.call_count, 1)
        self.assertEqual(self.mock_check_for_injections.call_count, 1)
        self.assertFalse(mock_create_user_database.called)

    def test_create_normal_user_no_create_db(self):
        create_user_query = 'GRANT %s to %s'

        username = 'username'
        password = 'password'

        self.backend.create_user(username, password, create_db=False)
        params = (PUBLIC_ROLE, username)
        mock_create_user_database = self.create_patch(
            'core.db.backend.pg.PGBackend.create_user_database')

        # import pdb; pdb.set_trace()
        self.assertEqual(
            self.mock_execute_sql.call_args[0][0], create_user_query)
        self.assertEqual(self.mock_execute_sql.call_args[0][1], params)
        self.assertEqual(self.mock_as_is.call_count, 3)
        self.assertEqual(self.mock_check_for_injections.call_count, 1)
        self.assertFalse(mock_create_user_database.called)

    def test_create_user_calls_create_db(self):
        username = 'username'
        password = 'password'
        mock_create_user_database = self.create_patch(
            'core.db.backend.pg.PGBackend.create_user_database')

        self.backend.create_user(
            username=username, password=password, create_db=True)
        self.assertTrue(mock_create_user_database.called)

    def test_create_user_db(self):
        create_db_query_1 = 'CREATE DATABASE %s; '
        create_db_query_2 = 'ALTER DATABASE %s OWNER TO %s; '
        username = 'username'

        self.backend.create_user_database(username)
        params_1 = (username,)
        params_2 = (username, username)

        call_args_1 = self.mock_execute_sql.call_args_list[0][0]
        self.assertEqual(call_args_1[0], create_db_query_1)
        self.assertEqual(call_args_1[1], params_1)

        call_args_2 = self.mock_execute_sql.call_args_list[1][0]
        self.assertEqual(call_args_2[0], create_db_query_2)
        self.assertEqual(call_args_2[1], params_2)

        self.assertEqual(self.mock_as_is.call_count, len(params_1 + params_2))
        self.assertEqual(self.mock_check_for_injections.call_count, 1)

    def test_remove_user(self):
        query = 'DROP ROLE %s;'
        username = "username"
        params = (username,)
        self.backend.remove_user(username)

        self.assertEqual(
            self.mock_execute_sql.call_args[0][0], query)
        self.assertEqual(self.mock_execute_sql.call_args[0][1], params)
        self.assertEqual(self.mock_as_is.call_count, len(params))
        self.assertEqual(self.mock_check_for_injections.call_count, 1)

    def test_remove_database(self):
        # mock out list_all_users
        mock_list_all_users = self.create_patch(
            'core.db.backend.pg.PGBackend.list_all_users')
        mock_list_all_users.return_value = ['tweedledee', 'tweedledum']

        self.backend.remove_database(self.username)

        # revoke statement stuff
        revoke_query = 'REVOKE ALL ON DATABASE %s FROM %s;'
        revoke_params_1 = (self.username, 'tweedledee')
        revoke_params_2 = (self.username, 'tweedledum')

        self.assertEqual(
            self.mock_execute_sql.call_args_list[0][0][0], revoke_query)
        self.assertEqual(
            self.mock_execute_sql.call_args_list[0][0][1], revoke_params_1)

        self.assertEqual(
            self.mock_execute_sql.call_args_list[1][0][0], revoke_query)
        self.assertEqual(
            self.mock_execute_sql.call_args_list[1][0][1], revoke_params_2)

        # drop statement stuff
        drop_query = 'DROP DATABASE %s;'
        drop_params = (self.username,)

        self.assertEqual(
            self.mock_execute_sql.call_args_list[2][0][0], drop_query)
        self.assertEqual(
            self.mock_execute_sql.call_args_list[2][0][1], drop_params)
        self.assertEqual(self.mock_as_is.call_count, 5)
        self.assertEqual(self.mock_check_for_injections.call_count, 1)

    def test_change_password(self):
        query = 'ALTER ROLE %s WITH PASSWORD %s;'
        params = (self.username, self.password)
        self.backend.change_password(self.username, self.password)

        self.assertEqual(
            self.mock_execute_sql.call_args[0][0], query)
        self.assertEqual(self.mock_execute_sql.call_args[0][1], params)
        self.assertEqual(self.mock_as_is.call_count, 1)
        self.assertEqual(self.mock_check_for_injections.call_count, 1)

    def test_list_collaborators(self):
        query = 'SELECT unnest(nspacl) FROM pg_namespace WHERE nspname=%s;'
        repo = 'repo_name'
        params = (repo, )

        self.mock_execute_sql.return_value = {
            'status': True, 'row_count': 2,
            'tuples': [
                ('al_carter=UC/al_carter',),
                ('foo_bar=U/al_carter',)
            ],
            'fields': [{'type': 1033, 'name': 'unnest'}]}

        expected_result = [
            {'username': 'al_carter', 'db_permissions': 'UC'},
            {'username': 'foo_bar', 'db_permissions': 'U'}
            ]

        res = self.backend.list_collaborators(repo)

        self.assertEqual(
            self.mock_execute_sql.call_args[0][0], query)
        self.assertEqual(
            self.mock_execute_sql.call_args[0][1], params)
        self.assertFalse(self.mock_as_is.called)
        self.assertEqual(res, expected_result)

    def test_list_all_users(self):
        query = 'SELECT usename FROM pg_catalog.pg_user WHERE usename != %s'
        params = (self.username,)
        self.mock_execute_sql.return_value = {
            'status': True, 'row_count': 2,
            'tuples': [(u'delete_me_alpha_user',), (u'delete_me_beta_user',)],
            'fields': [{'type': 19, 'name': 'usename'}]
            }

        res = self.backend.list_all_users()

        self.assertEqual(
            self.mock_execute_sql.call_args[0][0], query)
        self.assertEqual(
            self.mock_execute_sql.call_args[0][1], params)
        self.assertFalse(self.mock_as_is.called)
        self.assertEqual(res, ['delete_me_alpha_user', 'delete_me_beta_user'])

    def test_has_base_privilege(self):
        query = 'SELECT has_database_privilege(%s, %s);'
        privilege = 'CONNECT'
        params = (self.username, privilege)
        self.mock_execute_sql.return_value = {'status': True, 'row_count': -1,
                                              'tuples': [[True]], 'fields': []}

        res = self.backend.has_base_privilege(
            login=self.username, privilege=privilege)

        self.assertEqual(
            self.mock_execute_sql.call_args[0][0], query)
        self.assertEqual(self.mock_execute_sql.call_args[0][1], params)
        self.assertEqual(self.mock_as_is.call_count, 0)
        self.assertEqual(res, True)

    def test_has_repo_db_privilege(self):
        query = 'SELECT has_schema_privilege(%s, %s, %s);'
        repo = 'repo'
        privilege = 'CONNECT'
        params = (self.username, repo, privilege)
        self.mock_execute_sql.return_value = {'status': True, 'row_count': -1,
                                              'tuples': [[True]], 'fields': []}

        res = self.backend.has_repo_db_privilege(
            login=self.username, repo=repo, privilege=privilege)

        self.assertEqual(
            self.mock_execute_sql.call_args[0][0], query)
        self.assertEqual(self.mock_execute_sql.call_args[0][1], params)
        self.assertEqual(self.mock_as_is.call_count, 0)
        self.assertEqual(res, True)

    def test_has_table_privilege(self):
        query = 'SELECT has_table_privilege(%s, %s, %s);'
        table = 'table'
        privilege = 'CONNECT'
        params = (self.username, table, privilege)
        self.mock_execute_sql.return_value = {'status': True, 'row_count': -1,
                                              'tuples': [[True]], 'fields': []}
        res = self.backend.has_table_privilege(
            login=self.username, table=table, privilege=privilege)

        self.assertEqual(
            self.mock_execute_sql.call_args[0][0], query)
        self.assertEqual(self.mock_execute_sql.call_args[0][1], params)
        self.assertEqual(self.mock_as_is.call_count, 0)
        self.assertEqual(res, True)

    def test_has_column_privilege(self):
        query = 'SELECT has_column_privilege(%s, %s, %s, %s);'
        table = 'table'
        column = 'column'
        privilege = 'CONNECT'
        params = (self.username, table, column, privilege)
        self.mock_execute_sql.return_value = {'status': True, 'row_count': -1,
                                              'tuples': [[True]], 'fields': []}

        res = self.backend.has_column_privilege(
            login=self.username, table=table,
            column=column, privilege=privilege)

        self.assertEqual(
            self.mock_execute_sql.call_args[0][0], query)
        self.assertEqual(self.mock_execute_sql.call_args[0][1], params)
        self.assertEqual(self.mock_as_is.call_count, 0)
        self.assertEqual(res, True)

    @patch('core.db.backend.pg.os.makedirs')
    @patch('core.db.backend.pg.os.remove')
    @patch('core.db.backend.pg.shutil.move')
    def test_export_table_with_header(self, *args):
        table_name = 'repo_name.table_name'
        table_name_prepped = 'SELECT * FROM %s' % table_name
        file_path = 'file_path'
        file_format = 'file_format'
        delimiter = ','
        header = True
        query = ('COPY (SELECT * FROM repo_name.table_name) '
                 'TO STDOUT WITH CSV HEADER DELIMITER \',\';')

        self.backend.connection = Mock()
        mock_connection = self.backend.connection
        mock_mogrify = mock_connection.cursor.return_value.mogrify
        mock_mogrify.return_value = query
        mock_copy_expert = mock_connection.cursor.return_value.copy_expert

        with patch("__builtin__.open", mock_open()):
            self.backend.export_table(table_name, file_path,
                                      file_format, delimiter, header)

        mock_mogrify.assert_called_once_with(
            'COPY (%s) TO STDOUT WITH %s %s DELIMITER %s;',
            (table_name_prepped, file_format,
             'HEADER' if header else '', delimiter))

        # Kind of a meaningless check since we have to mock the return value
        # of mogrify, but at least it ensures the result of mogrify is passed
        # into copy_expert as is.
        self.assertEqual(mock_copy_expert.call_args[0][0], query)
        self.assertEqual(self.mock_as_is.call_count, 3)
        self.assertEqual(self.mock_check_for_injections.call_count, 4)
        self.assertEqual(self.mock_validate_table_name.call_count, 1)

    @patch('core.db.backend.pg.os.makedirs')
    @patch('core.db.backend.pg.os.remove')
    @patch('core.db.backend.pg.shutil.move')
    def test_export_table_with_no_header(self, *args):
        table_name = 'repo_name.table_name'
        table_name_prepped = 'SELECT * FROM %s' % table_name
        file_path = 'file_path'
        file_format = 'file_format'
        delimiter = ','
        header = False
        query = ('COPY (SELECT * FROM repo_name.table_name) '
                 'TO STDOUT WITH CSV  DELIMITER \',\';')

        self.backend.connection = Mock()
        mock_connection = self.backend.connection
        mock_mogrify = mock_connection.cursor.return_value.mogrify
        mock_mogrify.return_value = query
        mock_copy_expert = mock_connection.cursor.return_value.copy_expert

        with patch("__builtin__.open", mock_open()):
            self.backend.export_table(table_name, file_path,
                                      file_format, delimiter, header)

        mock_mogrify.assert_called_once_with(
            'COPY (%s) TO STDOUT WITH %s %s DELIMITER %s;',
            (table_name_prepped, file_format,
             'HEADER' if header else '', delimiter))

        # Kind of a meaningless check since we have to mock the return value
        # of mogrify, but at least it ensures the result of mogrify is passed
        # into copy_expert as is.
        self.assertEqual(mock_copy_expert.call_args[0][0], query)
        self.assertEqual(self.mock_as_is.call_count, 3)
        self.assertEqual(self.mock_check_for_injections.call_count, 4)
        self.assertEqual(self.mock_validate_table_name.call_count, 1)

    @patch('core.db.backend.pg.os.makedirs')
    @patch('core.db.backend.pg.os.remove')
    @patch('core.db.backend.pg.shutil.move')
    def test_export_view(self, *args):
        view_name = 'repo_name.view_name'
        view_name_prepped = 'SELECT * FROM %s' % view_name
        file_path = 'file_path'
        file_format = 'file_format'
        delimiter = ','
        header = True
        query = ('COPY (SELECT * FROM repo_name.view_name) '
                 'TO STDOUT WITH CSV HEADER DELIMITER \',\';')

        self.backend.connection = Mock()
        mock_connection = self.backend.connection
        mock_mogrify = mock_connection.cursor.return_value.mogrify
        mock_mogrify.return_value = query
        mock_copy_expert = mock_connection.cursor.return_value.copy_expert

        with patch("__builtin__.open", mock_open()):
            self.backend.export_view(view_name, file_path,
                                     file_format, delimiter, header)

        mock_mogrify.assert_called_once_with(
            'COPY (%s) TO STDOUT WITH %s %s DELIMITER %s;',
            (view_name_prepped, file_format,
             'HEADER' if header else '', delimiter))

        # Kind of a meaningless check since we have to mock the return value
        # of mogrify, but at least it ensures the result of mogrify is passed
        # into copy_expert as is.
        self.assertEqual(mock_copy_expert.call_args[0][0], query)
        self.assertEqual(self.mock_as_is.call_count, 3)
        self.assertEqual(self.mock_check_for_injections.call_count, 4)
        self.assertEqual(self.mock_validate_table_name.call_count, 1)

    @patch('core.db.backend.pg.os.makedirs')
    @patch('core.db.backend.pg.os.remove')
    @patch('core.db.backend.pg.shutil.move')
    def _export_query_test_helper(self, *args, **kwargs):
        passed_query = kwargs['passed_query']
        passed_query_cleaned = kwargs.get(
            'passed_query_cleaned', passed_query)
        file_path = kwargs['file_path']
        file_format = kwargs['file_format']
        delimiter = kwargs['delimiter']
        header = kwargs['header']
        query = kwargs['query']

        self.backend.connection = Mock()
        mock_connection = self.backend.connection
        mock_mogrify = mock_connection.cursor.return_value.mogrify
        mock_mogrify.return_value = query
        mock_copy_expert = mock_connection.cursor.return_value.copy_expert

        with patch("__builtin__.open", mock_open()):
            self.backend.export_query(passed_query, file_path,
                                      file_format, delimiter, header)

        mock_mogrify.assert_called_once_with(
            'COPY (%s) TO STDOUT WITH %s %s DELIMITER %s;',
            (passed_query_cleaned, file_format,
             'HEADER' if header else '', delimiter))

        # Kind of a meaningless check since we have to mock the return value
        # of mogrify, but at least it ensures the result of mogrify is passed
        # into copy_expert as is.
        self.assertEqual(mock_copy_expert.call_args[0][0], query)
        self.assertEqual(self.mock_as_is.call_count, 3)
        self.assertEqual(self.mock_check_for_injections.call_count, 2)

    def test_export_query_with_header(self, *args):
        self._export_query_test_helper(
            passed_query='myquery',
            file_path='file_path',
            file_format='CSV',
            delimiter=',',
            header=True,
            query=('COPY (myquery) '
                   'TO STDOUT WITH CSV HEADER DELIMITER \',\';'))

    def test_export_query_with_no_header(self, *args):
        self._export_query_test_helper(
            passed_query='myquery',
            file_path='file_path',
            file_format='CSV',
            delimiter=',',
            header=False,
            query=('COPY (myquery) '
                   'TO STDOUT WITH CSV  DELIMITER \',\';'))

    def test_export_query_only_executes_text_before_semicolon(self, *args):
        self._export_query_test_helper(
            passed_query=' text before semicolon; text after; ',
            passed_query_cleaned='text before semicolon',
            file_path='file_path',
            file_format='CSV',
            delimiter=',',
            header=False,
            query=('COPY (text before semicolon) '
                   'TO STDOUT WITH CSV  DELIMITER \',\';'))

    def test_import_file_with_header(self):
        query = 'COPY %s FROM %s WITH %s %s DELIMITER %s ENCODING %s QUOTE %s;'
        table_name = 'user_name.repo_name.table_name'
        file_path = 'file_path'
        file_format = 'file_format'
        delimiter = ','
        header = True
        encoding = 'ISO-8859-1'
        quote_character = '"'

        params = (table_name, file_path, file_format,
                  'HEADER', delimiter, encoding, quote_character)
        self.backend.import_file(table_name, file_path, file_format, delimiter,
                                 header, encoding, quote_character)

        self.assertEqual(self.mock_execute_sql.call_args[0][0], query)
        self.assertEqual(self.mock_execute_sql.call_args[0][1], params)
        self.assertEqual(self.mock_as_is.call_count, 3)
        self.assertEqual(self.mock_check_for_injections. call_count, 3)
        self.assertEqual(self.mock_validate_table_name.call_count, 1)

    def test_import_table_with_no_header(self):
        table_name = 'table_name'
        file_path = 'file_path'
        file_format = 'file_format'
        delimiter = ','
        header = False
        encoding = 'ISO-8859-1'
        quote_character = '"'

        params = (table_name, file_path, file_format,
                  '', delimiter, encoding, quote_character)
        self.backend.import_file(table_name, file_path, file_format, delimiter,
                                 header, encoding, quote_character)
        self.assertEqual(self.mock_execute_sql.call_args[0][1], params)

    def test_import_file_w_dbtruck(self):
        # DBTruck is not tested for safety/security... At all.
        # The method does so little
        # that it doesn't even make much sense to test it.
        pass

    def test_can_user_access_rls_table(self):
        mock_settings = self.create_patch("core.db.backend.pg.settings")
        mock_settings.POLICY_SCHEMA = 'SCHEMA'
        mock_settings.POLICY_TABLE = 'TABLE'

        self.mock_execute_sql.return_value = {
            'status': True, 'row_count': 1,
            'tuples': [
                (True,),
            ]}

        username = 'delete_me_user'
        permissions = ['select', 'update']

        expected_query = (
            "SELECT exists("
            "SELECT * FROM %s.%s where grantee=lower(%s) and ("
            "lower(policy_type)=lower(%s) or lower(policy_type)=lower(%s)"
            "))")
        expected_params = ('SCHEMA', 'TABLE', 'delete_me_user', 'select',
                           'update')

        self.backend.can_user_access_rls_table(username, permissions)
        self.assertEqual(self.mock_execute_sql.call_args[0][0], expected_query)
        self.assertEqual(
            self.mock_execute_sql.call_args[0][1], expected_params)
