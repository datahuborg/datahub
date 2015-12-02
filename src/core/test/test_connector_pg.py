from mock import patch, Mock
import hashlib
import itertools

from django.test import TestCase
from django.test import Client

from inventory.models import User

from core.db.backend.pg import PGBackend
from core.db.manager import DataHubManager


# tests below this comment require authentication
# if these fail because a role/database already exists
# you will need to log into postgres and
# drop database username;
# drop role username;


class SchemaListCreateDeleteShare(TestCase):

    ''' tests that items reach the execute_sql method in pg.py.
        does not test execute_sql itself.
    '''

    def setUp(self):
        # some words to test out
        self.good_nouns = ['good', 'good_noun', 'good-noun']
        self.bad_nouns = ['_foo', 'foo_', '-foo', 'foo-', 'foo bar',
                          'injection;attack', ';injection', 'injection;',
                          ]

        # create the user... this should be moved to the new auth system
        # so that it stops being an integration test.
        self.username = "username"
        self.password = "password"
        # self.hashed_password = hashlib.sha1(self.password).hexdigest()
        # DataHubManager.create_user(username=self.username, password=self.hashed_password)

        # user = User(username=self.username, email="noreply@mit.edu",
        #     password=self.hashed_password)
        # user.save()

        # log the user in
        # login_credentials = {'login_id': self.username,
        # 'login_password': self.password}
        # self.client.post('/account/login', login_credentials)

        # mock the execute_sql function
        self.mock_execute_sql = self.create_patch(
            'core.db.backend.pg.PGBackend.execute_sql')
        self.mock_execute_sql.return_value = True

        # mock the psycopg2.extensions.AsIs, which many of the pg.py methods use
        # Its return value (side effect) is the call value
        self.mock_as_is = self.create_patch('core.db.backend.pg.AsIs')
        self.mock_as_is.side_effect = lambda x: x

        # create an instance of PGBackend
        self.backend = PGBackend(self.username,
                                 self.password,
                                 repo_base=self.username)

    def tearDown(self):
        DataHubManager.remove_user_and_database(username=self.username)

    def create_patch(self, name):
        # helper method for creating patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

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
            self.assertTrue(self.mock_as_is.called, True)

    def test_create_repo_sad_path(self):
        for noun in self.bad_nouns:
            with self.assertRaises(ValueError):
                self.backend.create_repo(noun)
            self.assertFalse(self.mock_execute_sql.called)

    def test_list_repo(self):
        # the user is already logged in, so there's not much to be tested ehre
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

    def test_delete_repo_happy_path_no_cascade(self):
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

    def test_delete_repo_sad_path(self):
        for noun in self.bad_nouns:
            with self.assertRaises(ValueError):
                self.backend.delete_repo(noun)
            self.assertFalse(self.mock_execute_sql.called)

    def test_add_collaborator_happy_path_auto_in_future(self):
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
                                    self.good_nouns, privileges
                                    )

        # test every combo here. For now, don't test combined priviledges
        for repo, sender, receiver, privilege in product:
            params = (repo, receiver, privilege, repo, receiver,
                      repo, privilege, receiver)

            self.backend.add_collaborator(
                sender, receiver, [privilege])

            self.assertTrue(
                self.mock_execute_sql.call_args[0][0], add_collab_query)
            self.assertTrue(self.mock_execute_sql.call_args[0][1], params)
            self.assertTrue(self.mock_as_is.call_count == len(params))

            self.mock_execute_sql.reset_mock()
            self.mock_as_is.reset_mock()
