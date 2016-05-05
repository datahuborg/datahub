from config import settings
from django.contrib.auth.models import User
import os
import core.db.connection


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


class _superuser_connection():
    superuser_con = None

    def __init__(self, repo_base=None):
        self.repo_base = repo_base

    def __enter__(self):
        self.superuser_con = core.db.connection.DataHubConnection(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            repo_base=self.repo_base)
        return self.superuser_con

    def __exit__(self, type, value, traceback):
        self.superuser_con.close_connection()


class RowLevelSecurityManager:

    def __init__(self, username, repo_base, repo, table):

        self.username = username
        self.repo_base = repo_base
        self.repo = repo
        self.table = table

        self.user_con = core.db.connection.DataHubConnection(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['USER'],
            repo_base='dh_public')

    def add_security_policy(self, policy, policy_type, grantee):
        '''
        Creates a new security policy in the policy table. First, we check
        whether this policy exists in the table. If so, return an error.
        Otherwise, create the policy.
        '''
        return self.user_con.create_security_policy(
            policy=policy,
            policy_type=policy_type,
            grantee=grantee,
            grantor=self.username,
            repo_base=self.repo_base,
            repo=self.repo,
            table=self.table)

    def list_security_policies(self):
        '''
        Returns a list of all the security policies defined on the table.
        '''
        return self.user_con.list_security_policies(
            self.table, self.repo, self.repo_base)

    def find_security_policy(self, policy_id=None, policy=None,
                             policy_type=None, grantee=None, grantor=None):
        '''
        Looks for security policies matching what the user specified in
        the input.
        '''
        return self.user_con.find_security_policy(
            self.table, self.repo, self.repo_base, policy_id, policy,
            policy_type, grantee, grantor)

    def find_security_policy_by_id(self, policy_id):
        '''
        Looks for a security policy matching the specified policy_id.
        '''
        return self.user_con.find_security_policy_by_id(policy_id)

    def update_security_policy(self, policy_id, new_policy, new_policy_type,
                               new_grantee):
        '''
        Updates the existing security policy with the specified inputs.
        '''
        return self.user_con.update_security_policy(
            policy_id, new_policy, new_policy_type, new_grantee)

    def remove_security_policy(self, policy_id):
        '''
        Removes the security policy specified by the policy_id.
        '''
        return self.user_con.remove_security_policy(policy_id)

    """
    static methods don't require permissions
    """

    @staticmethod
    def add_user_to_policy_table(username):
        """
        grant a user permission to select, insert, and update their own rows
        in the Row Level Security policy table.

        These rows are now owned by the superuser, so only the superuser can
        remove them.
        """
        policy = ('grantor = \'%s\'' % username)
        grantee = username
        grantor = settings.DATABASES['default']['USER']
        repo_base = settings.POLICY_DB
        repo = settings.POLICY_SCHEMA
        table = settings.POLICY_TABLE

        with _superuser_connection(repo_base=settings.POLICY_DB) as conn:
            # allow select
            conn.create_security_policy(
                policy=policy,
                policy_type="select",
                grantee = grantee,
                grantor = grantor,
                repo_base = repo_base,
                repo=repo,
                table=table)

            conn.create_security_policy(
                policy=policy,
                policy_type="insert",
                grantee = grantee,
                grantor = grantor,
                repo_base = repo_base,
                repo=repo,
                table=table)

            conn.create_security_policy(
                policy=policy,
                policy_type="update",
                grantee = grantee,
                grantor = grantor,
                repo_base = repo_base,
                repo=repo,
                table=table)


    @staticmethod
    def remove_user_from_policy_table(username):
        with _superuser_connection(settings.POLICY_DB) as conn:
            pass
