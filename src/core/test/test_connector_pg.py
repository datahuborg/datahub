from mock import patch, Mock
import hashlib
import itertools

from django.test import TestCase
from django.test import Client

from inventory.models import User

from core.db.backend.pg import PGBackend
from core.db.manager import DataHubManager


class HelperMethods(TestCase):
    ''' tests connections, validation and execution methods in PGBackend'''

    def setUp(self):
        # some words to test out
        self.good_nouns = ['good', 'good_noun', 'good-noun']

        # some words that shoudl throw validation errors
        self.bad_nouns = ['_foo', 'foo_', '-foo', 'foo-', 'foo bar',
                          'injection;attack', ';injection', 'injection;',
                          ]

        self.username = "username"
        self.password = "password"

        # self.mock_psychopg = self.create_patch('core.db.backend.pg.psycopg2')
        self.backend = PGBackend(self.username,
                                 self.password,
                                 repo_base=self.username)


    def create_patch(self, name):
        # helper method for creating patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def check_for_injections(self):
        ''' tests  validation against some sql injection attacks'''

        for noun in self.bad_nouns:
            with self.assertRaises(ValueError):
                self.backend._check_for_injections(noun)

        for noun in self.good_nouns:
            try:
                self.backend._check_for_injections(noun)
            except ValueError:
                self.fail('check_for_injections failed to verify a good name')


    # def test_execute_sql_strips_queries(self):
    #     mock_connection = self.create_patch(
    #         'core.db.backend.pg.PGBackend.__open_connection__')


    #     query = ' This query needs stripping; '
    #     self.backend.execute_sql(query)

    #     self.assertTrue(True) 


class SchemaListCreateDeleteShare(TestCase):

    ''' tests that items reach the execute_sql method in pg.py.
        does not test execute_sql itself.
    '''

    def setUp(self):
        # some words to test out
        self.good_nouns = ['good', 'good_noun', 'good-noun']
        # some words that shoudl throw validation errors
        self.bad_nouns = ['_foo', 'foo_', '-foo', 'foo-', 'foo bar',
                          'injection;attack', ';injection', 'injection;',
                          ]

        self.username = "username"
        self.password = "password"

        # mock the execute_sql function
        self.mock_execute_sql = self.create_patch(
            'core.db.backend.pg.PGBackend.execute_sql')
        self.mock_execute_sql.return_value = True

        # mock the is_valid_noun_name, which checks for injection attacks
        self.mock_check_for_injections = self.create_patch(
            'core.db.backend.pg.PGBackend._check_for_injections')

        # mock the psycopg2.extensions.AsIs, which many of the pg.py methods use
        # Its return value (side effect) is the call value
        self.mock_as_is = self.create_patch('core.db.backend.pg.AsIs')
        self.mock_as_is.side_effect = lambda x: x

        # create an instance of PGBackend
        self.backend = PGBackend(self.username,
                                 self.password,
                                 repo_base=self.username)

    def create_patch(self, name):
        # helper method for creating patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def reset_mocks(self):
        # clears the mock call arguments and sets their call counts to 0
        self.mock_as_is.reset_mock()
        self.mock_execute_sql.reset_mock()
        self.mock_check_for_injections.reset_mock()

    # testing externally called methods in PGBackend
    def test_create_repo_happy_path(self):
        create_repo_sql = 'CREATE SCHEMA IF NOT EXISTS %s AUTHORIZATION %s'

        for noun in self.good_nouns:
            self.backend.create_repo(noun)
            self.assertEqual(
                self.mock_execute_sql.call_args[0][0], create_repo_sql)
            self.assertEqual(
                self.mock_execute_sql.call_args[0][1][0], noun)
            self.assertEqual(
                self.mock_execute_sql.call_args[0][1][1], self.username)

            self.assertTrue(self.mock_as_is.called)
            self.assertTrue(self.mock_check_for_injections.called)

            # reset mocks
            self.reset_mocks()

    def test_list_repo(self):
        # the user is already logged in, so there's not much to be tested here
        # except that the arguments are passed correctly
        list_repo_sql = ('SELECT schema_name AS repo_name '
                         'FROM information_schema.schemata '
                         'WHERE schema_owner = %s')
        self.backend.list_repos()
        self.assertEqual(
            self.mock_execute_sql.call_args[0][0], list_repo_sql)
        self.assertEqual(
            self.mock_execute_sql.call_args[0][1][0], self.username)

    def test_delete_repo_happy_path_cascade(self):
        drop_schema_sql = 'DROP SCHEMA %s %s'
        for noun in self.good_nouns:
            self.backend.delete_repo(repo=noun, force=True)
            self.assertEqual(
                self.mock_execute_sql.call_args[0][0], drop_schema_sql)
            self.assertEqual(
                self.mock_execute_sql.call_args[0][1][0], noun)
            self.assertEqual(
                self.mock_execute_sql.call_args[0][1][1], 'CASCADE')
            self.assertTrue(self.mock_as_is.called)
            self.assertTrue(self.mock_check_for_injections)

            self.reset_mocks()

    def test_delete_repo_no_cascade(self):
        drop_schema_sql = 'DROP SCHEMA %s %s'
        for noun in self.good_nouns:
            self.backend.delete_repo(repo=noun, force=False)
            self.assertEqual(
                self.mock_execute_sql.call_args[0][0], drop_schema_sql)
            self.assertEqual(
                self.mock_execute_sql.call_args[0][1][0], noun)
            self.assertEqual(
                self.mock_execute_sql.call_args[0][1][1], None)
            self.assertTrue(self.mock_as_is.called)
            self.assertTrue(self.mock_check_for_injections.called)

            self.reset_mocks()

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

        

        product = itertools.product(self.good_nouns, self.good_nouns,
                                    privileges)

        # test every combo here. For now, don't test combined priviledges

        for repo, receiver, privilege in product:

            params = (repo, receiver, privilege, repo, receiver,
                      repo, privilege, receiver)

            
            self.backend.add_collaborator(
                repo=repo, username=receiver, privileges=[privilege])

            self.assertTrue(
                self.mock_execute_sql.call_args[0][0], add_collab_query)
            self.assertTrue(self.mock_execute_sql.call_args[0][1], params)
            self.assertTrue(self.mock_as_is.call_count == len(params))

            self.assertEqual(self.mock_check_for_injections.call_count, 3)

            self.reset_mocks()

    # def test_add_collaborator_concatinates_privileges(self):
    #     privileges = ['SELECT', 'USAGE']
    #     repo = 'repo'
    #     sender = 'sender'
    #     receiver = 'receiver'

    #     self.backend.add_collaborator(repo=repo, username=)
