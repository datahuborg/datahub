import factory

from django.db.models import signals
from django.core.management.base import BaseCommand

from config import settings
from core.db.manager import DataHubManager
from core.db.rlsmanager import RowLevelSecurityManager


class Command(BaseCommand):
    help = ("Creates the public policy schema and table "
            "necessary for creating row level security policies.")

    def handle(self, *args, **options):
        print('Creating the public policy schema')
        create_policy_schema(None, None)

        print('Creating the public policy table')
        create_policy_table(None, None)


@factory.django.mute_signals(signals.pre_save)
def create_policy_schema(apps, schema_editor):
    # create the dh_public schema if it doesn't exist
    public_username = settings.PUBLIC_ROLE
    datahub_manager = DataHubManager(public_username)

    create_schema_query = ('CREATE SCHEMA IF NOT EXISTS dh_public')
    datahub_manager.execute_sql(create_schema_query)


@factory.django.mute_signals(signals.pre_save)
def create_policy_table(apps, schema_editor):
    # create the policy table inside dh_public if it doesn't exist
    public_username = settings.PUBLIC_ROLE
    datahub_manager = DataHubManager(public_username)

    create_table_query = ('CREATE TABLE IF NOT EXISTS dh_public.policy'
                          '('
                          'policy_id serial primary key,'
                          'policy VARCHAR(80) NOT NULL,'
                          'policy_type VARCHAR(80) NOT NULL,'
                          'grantee VARCHAR(80) NOT NULL,'
                          'grantor VARCHAR(80) NOT NULL,'
                          'table_name VARCHAR(80) NOT NULL,'
                          'repo VARCHAR(80) NOT NULL,'
                          'repo_base VARCHAR(80) NOT NULL'
                          ');')
    datahub_manager.execute_sql(create_table_query)


def add_existing_users_to_security_policy_table(apps, schema_editor):
    '''
    give existing DH users access to the RLS policy table
    '''
    all_users = DataHubManager.list_all_users()

    # filter out the public and anonymous users
    all_users = [username for username in all_users if (
        username != settings.PUBLIC_ROLE and
        username != settings.ANONYMOUS_ROLE)
    ]

    # give users select/update/insert access to their rows in the  policy table
    for username in all_users:
        if not RowLevelSecurityManager.can_user_access_rls_table(username):
            RowLevelSecurityManager.add_user_to_policy_table(username)
