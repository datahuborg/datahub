from random import shuffle

from core.db.manager import RowLevelSecurityManager
from core.db.manager import DataHubManager, PermissionDenied

from django.contrib.auth.models import User
from django.test import TestCase
from django.conf import settings


class RLSManagerIntegrationTests(TestCase):
    """Tests RLS query rewriting"""

    owner_username = "delete_me_owner_username"
    owner_password = "delete_me_owner_password"
    owner_email = "{0}@datahub.csail.mit.edu".format(owner_username)

    other_username = "delete_me_other_username"
    other_password = "delete_me_other_password"
    other_email = "{0}@datahub.csail.mit.edu".format(other_username)

    private_repo = 'private_repo'
    shared_repo = 'shared_repo'
    public_repo = 'public_repo'
    repos = [public_repo, shared_repo, private_repo]

    table1 = 'table1'
    table2 = 'table2'
    tables = [table1, table2]

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
        # create some repos, tables, and views
        with DataHubManager(user=self.owner_username,
                            repo_base=self.owner_username) as m:
            for repo in self.repos:
                m.create_repo(repo)

                for table in self.tables:
                    query = ("Create table %s.%s "
                             "(id integer, words text) ") % (repo, table)
                    m.execute_sql(query)

                    for i in range(1, 20):
                        chicken = ['c', 'h', 'i', 'c', 'k', 'e', 'n']
                        shuffle(chicken)
                        chicken = ''.join(chicken)

                        query = ('insert into %s.%s values(%i, \'%s\')'
                                 % (repo, table, i, chicken))
                        m.execute_sql(query)

            # make the appropriate repos shared/public
            m.add_collaborator(repo=self.shared_repo,
                               collaborator=self.other_username,
                               db_privileges=['SELECT'],
                               file_privileges=['read'])
            m.add_collaborator(repo=self.public_repo,
                               collaborator=settings.PUBLIC_ROLE,
                               db_privileges=['SELECT'],
                               file_privileges=['read'])

    def tearDown(self):
        self.delete_all_test_users()

    # Private Repo #
    def test_private_repo_rls_does_not_grant_access(self):
        """
        Allowing someone to select via RLS does not override DB Grants.
        So even if the OWNER of a repo enables a COLLABORATOR to SELECT from a
        table, if they haven't added COLLABORATOR via add_collaborator/the DB
        Their RLS share is overridden
        """
        # Grant access to the table in RLS, but not via a DB grant
        RowLevelSecurityManager.create_security_policy(
            policy="True", policy_type="Select", grantee=self.other_username,
            grantor=self.owner_username, repo_base=self.owner_username,
            repo=self.private_repo, table=self.table1, safe=True)

        # Try to access the repo
        with DataHubManager(user=self.other_username,
                            repo_base=self.owner_username) as m:
            with self.assertRaises(PermissionDenied):
                m.execute_sql('select * from private_repo.table1;')

    # Shared Repo #
    def test_shared_repo_rls_restricted_access(self):
        '''
        share a repo, and then restrict access to one of its tables, using rls
        '''

        # other_username is already granted access to shared_repo in self.setUp

        # restrict other_username's access to just the row where id=2
        RowLevelSecurityManager.create_security_policy(
            policy="id=2", policy_type="select", grantee=self.other_username,
            grantor=self.owner_username, repo_base=self.owner_username,
            repo=self.shared_repo, table=self.table1, safe=True)

        # see what other_username can access
        with DataHubManager(user=self.other_username,
                            repo_base=self.owner_username) as m:
            res = m.execute_sql('select id, words from shared_repo.table1;')

        self.assertEqual(res['tuples'][0][0], 2)

    def test_shared_repo_rls_restricted_access_with_capital_policy(self):
        '''
        same as the above test, but uses a capital 'SELECT' policy type,
        which has caused trouble in the past
        '''
        # other_username is already granted access to shared_repo in self.setUp

        # restrict other_username's access to just the row where id=2
        RowLevelSecurityManager.create_security_policy(
            policy="id=2", policy_type="SELECT", grantee=self.other_username,
            grantor=self.owner_username, repo_base=self.owner_username,
            repo=self.shared_repo, table=self.table1, safe=True)

        # see what other_username can access
        with DataHubManager(user=self.other_username,
                            repo_base=self.owner_username) as m:
            res = m.execute_sql('select id, words from shared_repo.table1;')

        self.assertEqual(res['tuples'][0][0], 2)

    # Public Repo #
    def test_public_repo_restricted_access_w_authenticated_collab(self):
        '''
        a policy applied to the public role should NOT affect a share that's
        made explicitly with a specific user
        '''
        RowLevelSecurityManager.create_security_policy(
            policy="id=2", policy_type="SELECT", grantee=settings.PUBLIC_ROLE,
            grantor=self.owner_username, repo_base=self.owner_username,
            repo=self.shared_repo, table=self.table1, safe=True)

        # see what other_username can access
        with DataHubManager(user=self.other_username,
                            repo_base=self.owner_username) as m:
            res = m.execute_sql('select id, words from shared_repo.table1;')

        # the authenticated user should see more than the one record that the
        # public user is limited to
        self.assertTrue(len(res['tuples']) > 1)

    def test_public_repo_restricted_access_w_unauthenticated_noncollab(self):
        '''
        a policy applied to the public role SHOULD affect anonymous users
        '''
        RowLevelSecurityManager.create_security_policy(
            policy="id=2", policy_type="SELECT", grantee=settings.RLS_PUBLIC,
            grantor=self.owner_username, repo_base=self.owner_username,
            repo=self.public_repo, table=self.table1, safe=True)

        # see the unauthenticated user can access
        with DataHubManager(user=settings.ANONYMOUS_ROLE,
                            repo_base=self.owner_username) as m:
            res = m.execute_sql('select id, words from public_repo.table1;')

        # the authenticated user should see more than the one record that the
        # public user is limited to
        self.assertTrue(len(res['tuples']) == 1)

    def test_public_repo_restricted_access_w_authenticated_noncollab(self):
        '''
        a policy applied to the public role SHOULD affect authenticated users
        with whom the share has not been made explicit
        '''
        RowLevelSecurityManager.create_security_policy(
            policy="id=2", policy_type="SELECT", grantee=settings.RLS_PUBLIC,
            grantor=self.owner_username, repo_base=self.owner_username,
            repo=self.public_repo, table=self.table1, safe=True)

        # see what other_username can access
        with DataHubManager(user=self.other_username,
                            repo_base=self.owner_username) as m:
            res = m.execute_sql('select id, words from public_repo.table1;')

        # the authenticated user should see more than the one record that the
        # public user is limited to
        self.assertTrue(len(res['tuples']) == 1)
