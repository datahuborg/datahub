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

    @staticmethod
    def find_licenses():
        # Returns all licenses
        with _superuser_connection(settings.LICENSE_DB) as conn:
            res = conn.find_licenses()

        # convert this to a named tuple for easier handling
        tuple_licenses = []
        for license in res:
            License = namedtuple(
                        'License',
                        [
                            'license_id', 'license_name', 'pii_def',
                            'pii_anonymized', 'pii_removed'
                        ]
                    )

            tuple_license = License(*license)

            tuple_licenses.append(tuple_license)

        return tuple_licenses

    @staticmethod
    def find_license_by_id(license_id):
        '''
        Looks for a license matching the specified license_id.
        '''
        license_id = int(license_id)

        with _superuser_connection(settings.LICENSE_DB) as conn:
            res = conn.find_license_by_id(license_id=license_id)

        License = namedtuple(
                        'License',
                        [
                            'license_id', 'license_name', 'pii_def',
                            'pii_anonymized', 'pii_removed'
                        ]
                    )
        tuple_license = License(*res)
        return tuple_license

    @staticmethod
    def find_licenses_by_repo(repo_base, repo):
        '''
        Find Licenses based on a given repo_base and repo
        '''
        license_links = LicenseManager.find_license_links_by_repo(
            repo_base, repo)

        licenses = []
        with _superuser_connection(settings.LICENSE_DB) as conn:

            for license_link in license_links:
                license_id = license_link.license_id
                res = conn.find_license_by_id(license_id)

                License = namedtuple(
                            'License',
                            [
                                'license_id', 'license_name',
                                'pii_def', 'pii_anonymized', 'pii_removed'
                            ]
                        )

                tuple_license = License(*res)

                licenses.append(tuple_license)

        return licenses

    @staticmethod
    def create_license(license_name, pii_def, pii_anonymized, pii_removed):
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
                pii_removed=pii_removed)

    @staticmethod
    def create_license_link(repo_base, repo, license_id):
        '''
        Links a license to a repo
        '''
        with _superuser_connection(settings.LICENSE_DB) as conn:
            return conn.create_license_link(
                repo_base=repo_base,
                repo=repo,
                license_id=license_id)

    @staticmethod
    def find_license_links(license_id):
        '''
        Returns all licenses links for a specified license id
        '''
        with _superuser_connection(settings.LICENSE_DB) as conn:
            res = conn.find_license_links(license_id)

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
        Finds LicenseLinks for a particular repo_base and repo
        '''
        with _superuser_connection(settings.LICENSE_DB) as conn:
            res = conn.find_license_links_by_repo(repo_base, repo)

        # convert this to a named tuple for easier handling
        tuple_license_links = []
        for license_link in res:
            LicenseLink = namedtuple(
                'LicenseLink',
                ['license_link_id', 'repo_base', 'repo', 'license_id'])

            tuple_license_link = LicenseLink(*license_link)

            tuple_license_links.append(tuple_license_link)

        return tuple_license_links
