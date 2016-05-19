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

    def list_security_policies(self, repo, table):
        '''
        Returns a list of all the security policies defined on the table.
        '''
        return self.user_con.list_security_policies(
            self.repo_base, repo, table)

    def update_security_policy(self, policy_id, new_policy, new_policy_type,
                               new_grantee):
        '''
        Updates the existing security policy with the specified inputs.

        Uses policy_id to locate the existing policy.
        '''
        return self.user_con.update_security_policy(
            policy_id, new_policy, new_policy_type, new_grantee)

    # def find_all_security_policies is not implemented in rlsmanager, because
    # it allows a user to view security policies that have been applied to
    # them.

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
        with _superuser_connection(settings.POLICY_DB) as conn:
            policies = conn.find_all_security_policies(username)
            for policy in policies:
                conn.remove_security_policy(policy[0])

    @staticmethod
    def can_user_access_rls_table(username,
                                  permissions=['SELECT', 'UPDATE', 'INSERT']):
        with _superuser_connection(settings.POLICY_DB) as conn:
            result = conn.can_user_access_rls_table(username, permissions)
        return result

    # looking up security policies
    @staticmethod
    def find_all_security_policies(username):
        with _superuser_connection(settings.POLICY_DB) as conn:
            result = conn.find_all_security_policies(username)
        return result

    @staticmethod
    def find_security_policies(repo_base, repo, table, policy_id=None,
                               policy=None, policy_type=None, grantee=None,
                               grantor=None):
        '''
        Looks for security policies matching what the user specified in
        the input.
        '''
        with _superuser_connection(settings.POLICY_DB) as conn:
            return conn.find_security_policies(
                repo_base=repo_base,
                repo=repo,
                table=table,
                policy_id=policy_id,
                policy=policy,
                policy_type=policy_type,
                grantee=grantee,
                grantor=grantor)

    @staticmethod
    def find_security_policy_by_id(policy_id):
        '''
        Looks for a security policy matching the specified policy_id.
        '''
        with _superuser_connection(settings.POLICY_DB) as conn:
            return conn.find_security_policy_by_id(policy_id)

    @staticmethod
    def create_security_policy(
            policy, policy_type, grantee, grantor, repo_base, repo, table):
        '''
        Creates a new security policy in the policy table. First, we check
        whether this policy exists in the table. If so, return an error.
        Otherwise, create the policy.
        '''
        # Does the policy exist?
        security_policies = RowLevelSecurityManager.find_security_policies(
            repo_base=repo_base, repo=repo, table=table, policy=policy,
            policy_type=policy_type, grantee=grantee, grantor=grantor
        )
        if security_policies != []:
            raise Exception('Security policy already exists in table.')

        # Is the user the table owner?
        if repo_base != grantor:
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

        # get the policy, and make sure it exists
        policy = RowLevelSecurityManager.find_security_policy_by_id(policy_id)
        if not policy:
            raise LookupError('Policy_ID %s does not exist.' % (policy_id))

        # check to make sure the user can actually do this
        if safe and (username != repo_base):
            raise Exception('%s does not have permission to delete security '
                            'policies on %s' % (username, repo_base))

        with _superuser_connection(settings.POLICY_DB) as conn:
            return conn.remove_security_policy(policy_id)
