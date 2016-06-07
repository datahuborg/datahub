from collections import namedtuple

from config import settings
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

    def __init__(self, username, repo_base):

        self.username = username
        self.repo_base = repo_base

        self.user_con = core.db.connection.DataHubConnection(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['USER'],
            repo_base='dh_public')

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close_connection()

    def close_connection(self):
        self.user_con.close_connection()

    """
    static methods don't require permissions
    """

    # Creating the schema & table
    @staticmethod
    def create_security_policy_schema():
        ''' Used to create the security policy schema on DataHub start '''
        repo_base = settings.POLICY_DB
        with _superuser_connection(repo_base) as conn:
            result = conn.create_security_policy_schema()
        return result

    @staticmethod
    def create_security_policy_table():
        ''' Used to create the security policy table on DataHub start '''
        repo_base = settings.POLICY_DB
        with _superuser_connection(repo_base) as conn:
            result = conn.create_security_policy_table()
        return result

    # managing users
    @staticmethod
    def add_user_to_policy_table(username):
        """
        grant a user permission to select, insert, and update their own rows
        in the Row Level Security policy table.

        These rows are now owned by the superuser, so only the superuser can
        remove them.
        """
        username = username.lower()
        policy = ('grantor = \'%s\'' % username)
        grantee = username
        grantor = settings.DATABASES['default']['USER']
        repo_base = settings.POLICY_DB
        repo = settings.POLICY_SCHEMA
        table = settings.POLICY_TABLE

        security_policies = RowLevelSecurityManager.find_security_policies(
            repo_base, repo=repo, table=table,
            policy=policy, policy_type=None,
            grantee=grantee, grantor=grantor, safe=False)

        # Skip if the user already has policies granted by the superuser.
        if len(security_policies) > 0:
            return

        with _superuser_connection(repo_base=settings.POLICY_DB) as conn:
            # allow select
            conn.create_security_policy(
                policy=policy,
                policy_type="select",
                grantee=grantee,
                grantor=grantor,
                repo_base=repo_base,
                repo=repo,
                table=table)

            conn.create_security_policy(
                policy=policy,
                policy_type="insert",
                grantee=grantee,
                grantor=grantor,
                repo_base=repo_base,
                repo=repo,
                table=table)

            conn.create_security_policy(
                policy=policy,
                policy_type="update",
                grantee=grantee,
                grantor=grantor,
                repo_base=repo_base,
                repo=repo,
                table=table)

    @staticmethod
    def remove_user_from_policy_table(username):
        username = username.lower()
        with _superuser_connection(settings.POLICY_DB) as conn:
            policies = conn.find_all_security_policies(username)
            for policy in policies:
                conn.remove_security_policy(policy[0])

    @staticmethod
    def can_user_access_rls_table(username,
                                  permissions=['SELECT', 'UPDATE', 'INSERT']):
        username = username.lower()
        with _superuser_connection(settings.POLICY_DB) as conn:
            result = conn.can_user_access_rls_table(username, permissions)
        return result

    @staticmethod
    def find_all_security_policies(username):
        '''
        Find all security policies that are either granted to or granted by
        the passed username
        '''
        username = username.lower()
        with _superuser_connection(settings.POLICY_DB) as conn:
            result = conn.find_all_security_policies(username)
        return result

    @staticmethod
    def find_security_policies(repo_base, repo=None, table=None,
                               policy_id=None, policy=None, policy_type=None,
                               grantee=None, grantor=None, safe=True):
        '''
        Looks for security policies matching what the user specified in
        the input.
        '''
        repo_base = repo_base.lower()

        if safe and (repo_base != grantor):
            raise Exception('%s does not have permission to search security'
                            'policies on %s.%s.' % (grantor, repo, table))

        if repo:
            repo = repo.lower()
        if table:
            table = table.lower()
        if policy_id:
            policy_id = int(policy_id)
        if policy_type:
            policy_type = policy_type.lower()
        if grantee:
            grantee = grantee.lower()
        if grantor:
            grantor = grantor.lower()

        with _superuser_connection(settings.POLICY_DB) as conn:
            res = conn.find_security_policies(
                repo_base=repo_base,
                repo=repo,
                table=table,
                policy_id=policy_id,
                policy=policy,
                policy_type=policy_type,
                grantee=grantee,
                grantor=grantor)

        # convert this to a named tuple for easier handling
        tuple_policies = []
        for policy in res:
            Policy = namedtuple(
                'Policy',
                ['id', 'policy', 'policy_type', 'grantee', 'grantor',
                 'repo_base' 'repo', 'table'])

            tuple_policy = Policy(*policy)

            tuple_policies.append(tuple_policy)

        return tuple_policies

    @staticmethod
    def find_security_policy_by_id(policy_id):
        '''
        Looks for a security policy matching the specified policy_id.
        '''
        policy_id = int(policy_id)
        with _superuser_connection(settings.POLICY_DB) as conn:
            res = conn.find_security_policy_by_id(policy_id=policy_id)
        Policy = namedtuple(
            'Policy',
            ['id', 'policy', 'policy_type', 'grantee', 'grantor',
             'repo_base', 'repo', 'table'])
        tuple_policy = Policy(*res)

        return tuple_policy

    @staticmethod
    def create_security_policy(
            policy, policy_type, grantee, grantor, repo_base, repo, table,
            safe=True):
        '''
        Creates a new security policy in the policy table. First, we check
        whether this policy exists in the table. If so, return an error.
        Otherwise, create the policy.
        '''
        policy_type = policy_type.lower()
        grantee = grantee.lower()
        grantor = grantor.lower()
        repo_base = repo_base.lower()
        repo = repo.lower()
        table = table.lower()

        # Does the policy exist?
        security_policies = RowLevelSecurityManager.find_security_policies(
            repo_base=repo_base, repo=repo, table=table, policy=policy,
            policy_type=policy_type, grantee=grantee, grantor=grantor,
            safe=False
        )
        if security_policies != []:
            raise Exception('Security policy already exists in table.')

        # Is the user the table owner?
        if safe and (repo_base != grantor):
            raise Exception('%s does not have permission to define security '
                            'policies on %s.%s.' % (grantor, repo, table))

        with _superuser_connection(settings.POLICY_DB) as conn:
            return conn.create_security_policy(
                policy=policy,
                policy_type=policy_type,
                grantee=grantee,
                grantor=grantor,
                repo_base=repo_base,
                repo=repo,
                table=table)

    @staticmethod
    def remove_security_policy(
            policy_id, username=None, repo_base=None, safe=True):
        '''
        Removes the security policy specified by the policy_id.

        If safe is true, checks to make sure that the username==repo_base
        Else, skips the check, and deletes
        '''
        policy_id = int(policy_id)
        if username:
            username = username.lower()
        if repo_base:
            repo_base = repo_base.lower()

        # get the policy, and make sure it exists
        policy = RowLevelSecurityManager.find_security_policy_by_id(policy_id)
        if not policy:
            raise LookupError('Policy_ID %s does not exist.' % (policy_id))

        # check to make sure the user can actually do this
        if safe and (username != policy.grantor):
            raise Exception('%s does not have permission to delete security '
                            'policies on %s' % (username, policy.grantor))

        with _superuser_connection(settings.POLICY_DB) as conn:
            return conn.remove_security_policy(policy_id)

    @staticmethod
    def update_security_policy(policy_id, new_policy, new_policy_type,
                               new_grantee, username=None, safe=True):
        '''
        Updates the existing security policy with the specified inputs.

        Uses policy_id to locate the existing policy.

        if safe is true, makes sure that the policy's repo_base is the same
        as the username
        '''
        policy_id = int(policy_id)
        new_policy_type = new_policy_type.lower()
        new_grantee = new_grantee.lower()
        if username:
            username = username.lower()

        # get the policy, and make sure it exists
        policy = RowLevelSecurityManager.find_security_policy_by_id(policy_id)
        if not policy:
            raise LookupError('Policy_ID %s does not exist.' % (policy_id))

        # check to make sure the user can do this
        if safe and (username != policy.repo_base):
            raise Exception('%s does not have permission to update security '
                            'policies on %s'
                            % (username, policy.repo_base))

        with _superuser_connection(settings.POLICY_DB) as conn:
            return conn.update_security_policy(
                policy_id, new_policy, new_policy_type, new_grantee)
