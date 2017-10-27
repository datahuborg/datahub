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


class LicenseManager:

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
    def create_license_schema():
        ''' Used to create the license schema on DataHub start '''
        repo_base = settings.LICENSE_DB
        with _superuser_connection(repo_base) as conn:
            result = conn.create_license_schema()
        return result

    @staticmethod
    def create_license_table():
        ''' Used to create the license table on DataHub start '''
        print "got to creat license license manager"

        repo_base = settings.LICENSE_DB
        with _superuser_connection(repo_base) as conn:
            result = conn.create_license_table()
        return result

    @staticmethod
    def create_license_link_table():
        ''' Used to create the license table on DataHub start '''
        repo_base = settings.LICENSE_DB
        with _superuser_connection(repo_base) as conn:
            result = conn.create_license_link_table()
        return result

    # managing users
    # @staticmethod
    # def add_user_to_license_table(username):
    #     """
    #     grant a user permission to select, insert, and update their own rows
    #     in the Row Level Security policy table.

    #     These rows are now owned by the superuser, so only the superuser can
    #     remove them.
    #     """
    #     username = username.lower()
    #     policy = ('grantor = \'%s\'' % username)
    #     grantee = username
    #     grantor = settings.DATABASES['default']['USER']
    #     repo_base = settings.LICENSE_DB
    #     repo = settings.LICENSE_SCHEMA
    #     table = settings.LICENSE_TABLE

    #     # licenses = LicenseManager.find_security_policies(
    #     #     repo_base, repo=repo, table=table,
    #     #     policy=policy, policy_type=None,
    #     #     grantee=grantee, grantor=grantor, safe=False)

    #     # Skip if the user already has policies granted by the superuser.
    #     if len(licenses) > 0:
    #         return

    #     with _superuser_connection(repo_base=settings.POLICY_DB) as conn:
    #         # allow select
    #         conn.create_security_policy(
    #             policy=policy,
    #             policy_type="select",
    #             grantee=grantee,
    #             grantor=grantor,
    #             repo_base=repo_base,
    #             repo=repo,
    #             table=table)

    #         conn.create_security_policy(
    #             policy=policy,
    #             policy_type="insert",
    #             grantee=grantee,
    #             grantor=grantor,
    #             repo_base=repo_base,
    #             repo=repo,
    #             table=table)

    #         conn.create_security_policy(
    #             policy=policy,
    #             policy_type="update",
    #             grantee=grantee,
    #             grantor=grantor,
    #             repo_base=repo_base,
    #             repo=repo,
    #             table=table)


    # @staticmethod
    # def can_user_access_rls_table(username,
    #                               permissions=['SELECT', 'UPDATE', 'INSERT']):
    #     username = username.lower()
    #     with _superuser_connection(settings.POLICY_DB) as conn:
    #         result = conn.can_user_access_rls_table(username, permissions)
    #     return result

    # @staticmethod
    # def find_all_security_policies(username):
    #     '''
    #     Find all security policies that are either granted to or granted by
    #     the passed username
    #     '''
    #     username = username.lower()
    #     with _superuser_connection(settings.POLICY_DB) as conn:
    #         result = conn.find_all_security_policies(username)
    #     return result

    @staticmethod
    def find_licenses():
        '''
        Looks for security policies matching what the user specified in
        the input.
        '''
        
        with _superuser_connection(settings.LICENSE_DB) as conn:
            res = conn.find_licenses()

        # convert this to a named tuple for easier handling
        tuple_licenses = []
        for license in res:
            License = namedtuple(
                'License',
                ['license_id', 'license_name', 'pii_def', 'pii_anonymized', 'pii_removed'])

            tuple_license = License(*license)

            tuple_licenses.append(tuple_license)

        return tuple_licenses

    @staticmethod
    def find_license_by_id(license_id):
        '''
        Looks for a security policy matching the specified policy_id.
        '''
        license_id = int(license_id)
        print "in license manager with license id: ", license_id
        
        with _superuser_connection(settings.LICENSE_DB) as conn:
            print "got the conn"
            res = conn.find_license_by_id(license_id=license_id)
        
        print "in license manager with res: ", res

        License = namedtuple(
                'License',
                ['license_id', 'license_name', 'pii_def', 'pii_anonymized', 'pii_removed'])
        tuple_license = License(*res)
        print "tuple license: ", tuple_license
        return tuple_license

    @staticmethod
    def create_license(license_name, pii_def, pii_anonymized, pii_removed):
        print "we got to create"
        '''
        Creates a new license in the license table. 
        '''
        license_name = license_name.lower()
        pii_def = pii_def.lower()     

        with _superuser_connection(settings.LICENSE_DB) as conn:
            return conn.create_license(
                license_name=license_name,
                pii_def=pii_def,
                pii_anonymized=pii_anonymized,
                pii_removed=pii_removed,
                )

    @staticmethod
    def create_license_link(repo_base, repo, license_id):
        print "we got to create link"
        '''
        Creates a new license in the license table. 
        '''  

        with _superuser_connection(settings.LICENSE_DB) as conn:
            return conn.create_license_link(
                repo_base=repo_base,
                repo=repo,
                license_id=license_id
                )

    @staticmethod
    def find_license_links(license_id):
        '''
        Looks for security policies matching what the user specified in
        the input.
        '''
        with _superuser_connection(settings.LICENSE_DB) as conn:
             res = conn.find_license_links(license_id)

        print "res from find_ license _links: ", res
        # convert this to a named tuple for easier handling
        tuple_license_links = []
        for license_link in res:
            LicenseLink = namedtuple(
                'LicenseLink',
                ['license_link_id', 'repo_base', 'repo', 'license_id'])

            tuple_license_link = LicenseLink(*license_link)

            tuple_license_links.append(tuple_license_link)

        return tuple_license_links

    @staticmethod
    def find_license_links_by_repo(repo_base, repo):
        '''
        Looks for security policies matching what the user specified in
        the input.
        '''
        with _superuser_connection(settings.LICENSE_DB) as conn:
             res = conn.find_license_links_by_repo(repo_base, repo)

        print "res from find_ license _links repo: ", res
        # convert this to a named tuple for easier handling
        tuple_license_links = []
        for license_link in res:
            LicenseLink = namedtuple(
                'LicenseLink',
                ['license_link_id', 'repo_base', 'repo', 'license_id'])

            tuple_license_link = LicenseLink(*license_link)

            tuple_license_links.append(tuple_license_link)

        return tuple_license_links