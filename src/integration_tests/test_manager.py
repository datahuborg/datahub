from core.db.manager import DataHubManager
from core.db.errors import PermissionDenied
from psycopg2 import InternalError, ProgrammingError

from contextlib import contextmanager

from django.contrib.auth.models import User
from django.test import TestCase
from django.conf import settings


class ManagerIntegrationTests(TestCase):
    """Tests adding, removing, and modifying collaborators."""

    owner_username = "delete_me_owner_username"
    owner_password = "delete_me_owner_password"
    owner_email = "{0}@datahub.csail.mit.edu".format(owner_username)

    other_username = "delete_me_other_username"
    other_password = "delete_me_other_password"
    other_email = "{0}@datahub.csail.mit.edu".format(other_username)

    good_names = ['one', 'one1', 'one_1']
    bad_names = ['1one', '-one', 'one-1', '', ' ', ';']
    public_repos = ['public1', 'public2', 'public3', 'public4']
    expected_repos = ['full1', 'full2', 'full3', 'full4',
                      'empty1', 'empty2', 'empty3', 'empty4']
    expected_repos.extend(public_repos)
    expected_repos.extend(good_names)

    @classmethod
    def delete_all_test_users(cls):
        # When building tests, it's possible to delete some combination of the
        # django user/postgres user/postgres user database
        # This tries to catch the edge cases.
        all_users = DataHubManager.list_all_users()
        test_users = filter(lambda x: x.startswith('delete_me_'), all_users)
        for user in test_users:
            try:
                DataHubManager.remove_user(user, remove_db=True,
                                           ignore_missing_user=True)
            except:
                print('UNABLE TO DELETE USER ' + user)

        # Delete all django users whose name starts with 'delete_me_'.
        all_users = User.objects.all()
        test_users = all_users.filter(username__startswith='delete_me_')
        for user in test_users:
            user.delete()

    def setUp(self):
        # Start with a clean slate.
        self.delete_all_test_users()
        # create an owner
        self.owner = User.objects.create_user(
            self.owner_username, self.owner_email, self.owner_password)
        # create a potential collaborator
        self.other = User.objects.create_user(
            self.other_username, self.other_email, self.other_password)
        # create some repos, tables, views, cards, files
        with DataHubManager(user=self.owner_username,
                            repo_base=self.owner_username) as m:
            for i in xrange(1, 5):
                m.create_repo('empty%s' % i)
            for i in xrange(1, 5):
                repo = 'full%s' % i
                table = 'table1'
                view = 'view1'
                card = 'card1'
                m.create_repo(repo)
                m.create_table(
                    repo=repo,
                    table=table,
                    params=[{'column_name': 'column1', 'data_type': 'int'}])
                m.create_view(
                    repo=repo,
                    view=view,
                    sql='SELECT * from %s.%s' % (repo, table))
                m.create_card(
                    repo=repo,
                    card_name=card,
                    query='SELECT * from %s.%s' % (repo, table))
                m.export_table(
                    repo=repo,
                    table=table)
            for i in xrange(1, 5):
                repo = 'public%s' % i
                m.create_repo(repo)
                m.add_collaborator(
                    repo,
                    settings.PUBLIC_ROLE,
                    db_privileges=['SELECT'],
                    file_privileges=['READ'])

            for name in self.good_names:
                m.create_repo(name)

    def tearDown(self):
        self.delete_all_test_users()

    @contextmanager
    def _assertRaisesOrNone(self, exception, message=None):
        """
        Same as assertRaises, but works as a noop if passed None.

        Used to make tests easier to parameterize and reuse.

        Include message to show if unexpected Exception is raised.
        """
        try:
            if exception is not None:
                with self.assertRaises(exception):
                    yield
            else:
                yield
        except Exception as e:
            if message:
                print(message)
            raise e

    def test_repo_owner_errors(self):
        outcomes = {
            'create_valid': None,
            'create_invalid': ValueError,
            'repo_list': self.expected_repos,
            'collaborator_repo_list': [],
            'rename_valid_to_valid': None,
            'rename_non_existent_source': LookupError,
            'rename_to_existing_destination': ValueError,
            'rename_invalid_source': ValueError,
            'rename_invalid_destination': ValueError,
            'rename_public': None,
            'delete_valid': None,
            'delete_valid_with_dependents': InternalError,
            'delete_valid_with_dependents_and_force': None,
            'delete_invalid': ValueError,
            'delete_non_existent': LookupError,
            'delete_public': None,
        }

        with DataHubManager(user=self.owner_username,
                            repo_base=self.owner_username) as m:
            self.assertEqual(set(self.expected_repos), set(m.list_repos()))

        self._repo_collaborator_test_helper(self.owner_username, outcomes)

    def test_repo_non_collaborator_errors(self):
        outcomes = {
            'create_valid': PermissionDenied,
            'create_invalid': ValueError,
            'repo_list': self.public_repos,
            'collaborator_repo_list': [],
            'rename_valid_to_valid': PermissionDenied,
            'rename_non_existent_source': PermissionDenied,
            'rename_to_existing_destination': PermissionDenied,
            'rename_invalid_source': PermissionDenied,
            'rename_invalid_destination': PermissionDenied,
            'rename_public': PermissionDenied,
            'delete_valid': PermissionDenied,
            'delete_valid_with_dependents': PermissionDenied,
            'delete_valid_with_dependents_and_force': PermissionDenied,
            'delete_invalid': PermissionDenied,
            'delete_non_existent': PermissionDenied,
            'delete_public': PermissionDenied,
        }

        with DataHubManager(user=self.owner_username,
                            repo_base=self.owner_username) as m:
            self.assertEqual(set(self.expected_repos), set(m.list_repos()))

        self._repo_collaborator_test_helper(self.other_username, outcomes)

    def test_repo_errors_read_only_collaborator(self):
        collaborator_repos = [
            '%s.%s' % (self.owner_username, r)
            for r in ['full1']]
        outcomes = {
            'create_valid': PermissionDenied,
            'create_invalid': ValueError,
            'repo_list': ['full1'] + self.public_repos,
            'collaborator_repo_list': collaborator_repos,
            'rename_valid_to_valid': PermissionDenied,
            'rename_non_existent_source': PermissionDenied,
            'rename_to_existing_destination': PermissionDenied,
            'rename_invalid_source': PermissionDenied,
            'rename_invalid_destination': PermissionDenied,
            'rename_public': PermissionDenied,
            'delete_valid': PermissionDenied,
            'delete_valid_with_dependents': PermissionDenied,
            'delete_valid_with_dependents_and_force': PermissionDenied,
            'delete_invalid': PermissionDenied,
            'delete_non_existent': PermissionDenied,
            'delete_public': PermissionDenied,
        }

        with DataHubManager(user=self.owner_username,
                            repo_base=self.owner_username) as m:
            self.assertEqual(set(self.expected_repos), set(m.list_repos()))
            m.add_collaborator(
                repo='full1',
                collaborator=self.other_username,
                db_privileges=['select'],
                file_privileges=['read'])

        self._repo_collaborator_test_helper(self.other_username, outcomes)

    def test_repo_errors_read_write_collaborator(self):
        collaborator_repos = [
            '%s.%s' % (self.owner_username, r)
            for r in ['full1']]
        outcomes = {
            'create_valid': PermissionDenied,
            'create_invalid': ValueError,
            'repo_list': ['full1'] + self.public_repos,
            'collaborator_repo_list': collaborator_repos,
            'rename_valid_to_valid': PermissionDenied,
            'rename_non_existent_source': PermissionDenied,
            'rename_to_existing_destination': PermissionDenied,
            'rename_invalid_source': PermissionDenied,
            'rename_invalid_destination': PermissionDenied,
            'rename_public': PermissionDenied,
            'delete_valid': PermissionDenied,
            'delete_valid_with_dependents': PermissionDenied,
            'delete_valid_with_dependents_and_force': PermissionDenied,
            'delete_invalid': PermissionDenied,
            'delete_non_existent': PermissionDenied,
            'delete_public': PermissionDenied,
        }

        with DataHubManager(user=self.owner_username,
                            repo_base=self.owner_username) as m:
            self.assertEqual(set(self.expected_repos), set(m.list_repos()))
            m.add_collaborator(
                repo='full1',
                collaborator=self.other_username,
                db_privileges=['select', 'update', 'insert', 'delete'],
                file_privileges=['read', 'write'])
        self._repo_collaborator_test_helper(self.other_username, outcomes)

    def _repo_collaborator_test_helper(self, username, outcomes):
        """Try all varieties of creating, renaming, and deleting repos."""
        o = outcomes
        with DataHubManager(user=username,
                            repo_base=self.owner_username) as m:
            # Create with a valid name.
            for name in self.good_names:
                with self._assertRaisesOrNone(o['create_valid']):
                    m.create_repo(name)
            # Create with an invalid name.
            for name in self.bad_names:
                with self._assertRaisesOrNone(o['create_invalid']):
                    m.create_repo(name)
            self.assertEqual(set(o['repo_list']), set(m.list_repos()))
            collaborator_repos = [
                '%s.%s' % (c.repo_base, c.repo_name)
                for c in m.list_collaborator_repos()]
            self.assertEqual(set(o['collaborator_repo_list']),
                             set(collaborator_repos))

            self._repo_collaborator_test_helper_rename(outcomes, m)

            self._repo_collaborator_test_helper_delete(outcomes, m)

    def _repo_collaborator_test_helper_rename(self, outcomes, m):
        o = outcomes
        # Rename valid to valid
        with self._assertRaisesOrNone(o['rename_valid_to_valid']):
            m.rename_repo('full1', 'full11')
        # Rename non-existent
        with self._assertRaisesOrNone(o['rename_non_existent_source']):
            m.rename_repo('full1', 'full11')
        # Rename to taken name
        with self._assertRaisesOrNone(o['rename_to_existing_destination']):
            m.rename_repo('one1', 'full2')
        # Rename invalid source
        with self._assertRaisesOrNone(o['rename_invalid_source']):
            m.rename_repo('1one', 'one11')
        # Rename invalid destination
        with self._assertRaisesOrNone(o['rename_invalid_destination']):
            m.rename_repo('one1', '1one')
        # Rename public
        with self._assertRaisesOrNone(o['rename_public']):
            m.rename_repo('public1', 'public11')

    def _repo_collaborator_test_helper_delete(self, outcomes, m):
        o = outcomes
        # Delete valid
        with self._assertRaisesOrNone(o['delete_valid']):
            m.delete_repo('one_1')
        # Delete with dependents
        with self._assertRaisesOrNone(o['delete_valid_with_dependents']):
            m.delete_repo('full2')
        # Delete with dependents and force
        with self._assertRaisesOrNone(
                o['delete_valid_with_dependents_and_force']):
            m.delete_repo('full2', force=True)
        # Delete invalid
        with self._assertRaisesOrNone(o['delete_invalid']):
            m.delete_repo('1one')
        # Delete non-existent
        with self._assertRaisesOrNone(o['delete_non_existent']):
            m.delete_repo('one_1111')
        # Delete public
        with self._assertRaisesOrNone(o['delete_public']):
            m.delete_repo('public2')

    def test_create_table_as_owner_errors(self):
        repo = 'empty1'
        cases = [
            # Valid create_table
            (None, repo, 'table1',
             [{'column_name': 'column1', 'data_type': 'int'}]),
            # Invalid repo name
            (ValueError, '1repo', 'table2',
             [{'column_name': 'column1', 'data_type': 'int'}]),
            # Missing repo
            (LookupError, 'i_dont_exist', 'table2',
             [{'column_name': 'column1', 'data_type': 'int'}]),
            # Invalid table name
            (ValueError, repo, '1table',
             [{'column_name': 'column1', 'data_type': 'int'}]),
            # Taken table name
            (ValueError, repo, 'table1',
             [{'column_name': 'column1', 'data_type': 'int'}]),
            # Invalid column name
            (ValueError, repo, 'table2',
             [{'column_name': '1column', 'data_type': 'int'}]),
            # Reserved column name
            (ProgrammingError, repo, 'table2',
             [{'column_name': 'user', 'data_type': 'int'}]),
            # Invalid data type
            (ValueError, repo, 'table2',
             [{'column_name': 'column1', 'data_type': 'foo'}]),
            # Invalid params keys
            (KeyError, repo, 'table2',
             [{'foo': 'column1', 'data_type': 'int'}]),
            # Params iterable but not right structure
            (AttributeError, repo, 'table2',
             {'foo': 'int', 'bar': 'int'}),
            # Params not iterable
            (TypeError, repo, 'table2', 5),
        ]
        self._create_table_helper(
            self.owner_username, repo, cases, tables_after=['table1'])

    def test_create_table_as_public_errors(self):
        repo = 'public1'
        cases = [
            # Valid create_table
            (PermissionDenied, repo, 'table1',
             [{'column_name': 'column1', 'data_type': 'int'}]),
            # Invalid repo name
            (ValueError, '1repo', 'table2',
             [{'column_name': 'column1', 'data_type': 'int'}]),
            # Missing repo
            (LookupError, 'i_dont_exist', 'table2',
             [{'column_name': 'column1', 'data_type': 'int'}]),
            # Invalid table name
            (ValueError, repo, '1table',
             [{'column_name': 'column1', 'data_type': 'int'}]),
            # Taken table name
            (PermissionDenied, repo, 'table1',
             [{'column_name': 'column1', 'data_type': 'int'}]),
            # Invalid column name
            (ValueError, repo, 'table2',
             [{'column_name': '1column', 'data_type': 'int'}]),
            # Reserved column name
            (ProgrammingError, repo, 'table2',
             [{'column_name': 'user', 'data_type': 'int'}]),
            # Invalid data type
            (PermissionDenied, repo, 'table2',
             [{'column_name': 'column1', 'data_type': 'foo'}]),
            # Invalid params structure
            (KeyError, repo, 'table2',
             [{'foo': 'column1', 'data_type': 'int'}]),
            # Params iterable but not right structure
            (AttributeError, repo, 'table2',
             {'foo': 'int', 'bar': 'int'}),
            # Params not iterable
            (TypeError, repo, 'table2', 5),
        ]
        self._create_table_helper(
            settings.PUBLIC_ROLE, repo, cases, tables_after=[])

    def test_create_table_as_read_write_collaborator_errors(self):
        repo = 'empty1'
        cases = [
            # Valid create_table
            (PermissionDenied, repo, 'table1',
             [{'column_name': 'column1', 'data_type': 'int'}]),
            # Invalid repo name
            (ValueError, '1repo', 'table2',
             [{'column_name': 'column1', 'data_type': 'int'}]),
            # Missing repo
            (LookupError, 'i_dont_exist', 'table2',
             [{'column_name': 'column1', 'data_type': 'int'}]),
            # Invalid table name
            (ValueError, repo, '1table',
             [{'column_name': 'column1', 'data_type': 'int'}]),
            # Taken table name
            (PermissionDenied, repo, 'table1',
             [{'column_name': 'column1', 'data_type': 'int'}]),
            # Invalid column name
            (ValueError, repo, 'table2',
             [{'column_name': '1column', 'data_type': 'int'}]),
            # Reserved column name
            (ProgrammingError, repo, 'table2',
             [{'column_name': 'user', 'data_type': 'int'}]),
            # Invalid data type
            (PermissionDenied, repo, 'table2',
             [{'column_name': 'column1', 'data_type': 'foo'}]),
            # Invalid params structure
            (KeyError, repo, 'table2',
             [{'foo': 'column1', 'data_type': 'int'}]),
            # Params iterable but not right structure
            (AttributeError, repo, 'table2',
             {'foo': 'int', 'bar': 'int'}),
            # Params not iterable
            (TypeError, repo, 'table2', 5),
        ]
        with DataHubManager(user=self.owner_username,
                            repo_base=self.owner_username) as m:
            m.add_collaborator(
                repo='empty1',
                collaborator=self.other_username,
                db_privileges=['select', 'update', 'insert', 'delete'],
                file_privileges=['read', 'write'])

        self._create_table_helper(
            self.other_username, repo, cases, tables_after=[])

    def _create_table_helper(self, username, repo, cases, tables_after):
        """
        Tries to create a table in a repo as a user.

        Cases should be an array of test case tuples, where each tuple is the
        Exception to be raised or None plus the arguments to be passed to
        create_table.
        """
        with DataHubManager(user=username,
                            repo_base=self.owner_username) as m:
            self.assertEquals([], m.list_tables(repo))
            for c in cases:
                with self._assertRaisesOrNone(c[0], message=c):
                    m.create_table(*c[1:])
            self.assertEquals(tables_after, m.list_tables(repo))

    def test_list_table_errors(self):
        # List as owner
        with DataHubManager(user=self.owner_username,
                            repo_base=self.owner_username) as m:
            tables = m.list_tables('full1')
            self.assertEquals(set(tables), set(['table1']))
            with self._assertRaisesOrNone(LookupError):
                tables = m.list_tables('missing_repo')
                self.assertEquals(set(tables), set(['table1']))
            with self._assertRaisesOrNone(ValueError):
                tables = m.list_tables('1invalid repo')
                self.assertEquals(set(tables), set(['table1']))

            # Set up rest of test
            m.add_collaborator(
                repo='full2',
                collaborator=self.other_username,
                db_privileges=['select', 'update', 'insert', 'delete'],
                file_privileges=['read', 'write'])
            m.add_collaborator(
                repo='full3',
                collaborator=self.other_username,
                db_privileges=['select'],
                file_privileges=['read'])

        # List as public role
        with DataHubManager(user=settings.PUBLIC_ROLE,
                            repo_base=self.owner_username) as m:
            # Not a collaborator
            with self._assertRaisesOrNone(LookupError):
                m.list_tables('full1')
            tables = m.list_tables('public1')
            self.assertEquals(set(tables), set([]))

        # List as collaborator
        with DataHubManager(user=self.other_username,
                            repo_base=self.owner_username) as m:
            # Not a collaborator
            with self._assertRaisesOrNone(LookupError):
                m.list_tables('full1')
            # Readwrite collaborator
            tables = m.list_tables('full2')
            self.assertEquals(set(tables), set(['table1']))
            # Read-only collaborator
            tables = m.list_tables('full3')
            self.assertEquals(set(tables), set(['table1']))
            # Public collaborator
            tables = m.list_tables('public1')
            self.assertEquals(set(tables), set([]))

    def test_collaborator_errors(self):
        collaborator = self.other_username
        repo = 'full1'

        self._test_collaborator_errors_as_owner_helper(
            collaborator, repo)
        self._test_collaborator_errors_as_collaborator_helper(
            collaborator, repo)

    def _test_collaborator_errors_as_owner_helper(
            self, collaborator, repo):
        with DataHubManager(user=self.owner_username,
                            repo_base=self.owner_username) as m:
            # Add a read-only collaborator.
            m.add_collaborator(
                repo=repo,
                collaborator=collaborator,
                db_privileges=['select'],
                file_privileges=['read'])
            self.assertIn({
                'username': collaborator,
                'db_permissions': 'U',
                'file_permissions': 'read'},
                m.list_collaborators(repo))
            # Adding the same collaborator twice should fail.
            with self.assertRaises(ValueError):
                m.add_collaborator(
                    repo=repo,
                    collaborator=collaborator,
                    db_privileges=['select'],
                    file_privileges=['read', 'write'])
            # Delete a collaborator and they shouldn't be there anymore.
            m.delete_collaborator(
                repo=repo,
                collaborator=collaborator)
            self.assertNotIn(
                collaborator,
                (c['username'] for c in m.list_collaborators(repo)))
            # Add a collaborator with file but not db privileges
            # m.add_collaborator(
            #     repo=repo,
            #     collaborator=collaborator,
            #     db_privileges=None,
            #     file_privileges=['read', 'write'])
            # Add a collaborator with db but not file privileges
            # m.add_collaborator(
            #     repo=repo,
            #     collaborator=collaborator,
            #     db_privileges=['select'],
            #     file_privileges=None)

            # Make sure error conditions raise expected exceptions.
            with self.assertRaises(LookupError):
                m.add_collaborator(
                    repo='bad_repo_name',
                    collaborator=collaborator,
                    db_privileges=['select'],
                    file_privileges=['read'])
            with self.assertRaises(User.DoesNotExist):
                m.add_collaborator(
                    repo=repo,
                    collaborator='_invalid_user_name',
                    db_privileges=['select'],
                    file_privileges=['read'])
            with self.assertRaises(ValueError):
                m.add_collaborator(
                    repo=repo,
                    collaborator=collaborator,
                    db_privileges=['_invalid_db_privilege'],
                    file_privileges=['read'])
            with self.assertRaises(ValueError):
                m.add_collaborator(
                    repo=repo,
                    collaborator=collaborator,
                    db_privileges=['select'],
                    file_privileges=['_invalid_file_privilege'])

    def _test_collaborator_errors_as_collaborator_helper(
            self, collaborator, repo):
        with DataHubManager(user=collaborator,
                            repo_base=self.owner_username) as m:
            # Strangers shouldn't be able to add themselves as collaborators.
            with self.assertRaises(PermissionDenied):
                m.add_collaborator(
                    repo=repo,
                    collaborator=collaborator,
                    db_privileges=['select'],
                    file_privileges=['read'])
            # Or delete anyone from a repo.
            with self.assertRaises(PermissionDenied):
                m.delete_collaborator(
                    repo=repo,
                    collaborator=collaborator)
            with self.assertRaises(PermissionDenied):
                m.delete_collaborator(
                    repo=repo,
                    collaborator=self.owner_username)
