import factory

from django.db import IntegrityError
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from oauth2_provider.models import get_application_model

import sys
from config.settings import OAUTH2_APP_OWNER, OAUTH2_APP_CLIENTS
from core.db.manager import DataHubManager
from django.db.models import signals


class Command(BaseCommand):
    help = ("Creates the console OAuth2 application, and the related "
            "user/owner")

    def handle(self, *args, **options):
        print_if_not_testing('Creating the OAuth2 App Owner...')
        create_oauth2_user(None, None)
        print_if_not_testing('Creating the Console Application...')
        create_console_app(None, None)


@factory.django.mute_signals(signals.pre_save)
def create_oauth2_user(apps, schema_editor):
    """
    Create a user to own default oauth2 applications.
    This user has a django account, but not a database role/db, or data folder.
    """
    username = OAUTH2_APP_OWNER
    users = User.objects.filter(username=username)

    dh_user_exists = bool(len(users) > 0)
    db_exists = DataHubManager.database_exists(username)
    db_role_exists = DataHubManager.user_exists(username)
    user_data_folder_exists = DataHubManager.user_data_folder_exists(username)

    # try to create the django user. This skips validation, so the password
    # and email may as well be none.
    if not dh_user_exists:
        User.objects.create_user(
            username=username, email=None, password=None)
        print_if_not_testing('...django user created')

    # delete any db that exists
    if db_exists:
        DataHubManager.remove_database(
            repo_base=username, revoke_collaborators=True)
        print_if_not_testing('...db removed')

    # delete any db role that exists
    if db_role_exists:
        DataHubManager.remove_user(username, remove_db=False,
                                   ignore_missing_user=False)
        print_if_not_testing('...db role removed')

    # delete any user data folder that exists
    if user_data_folder_exists:
        DataHubManager.delete_user_data_folder(username)
        print_if_not_testing('...data folder removed')

    print_if_not_testing('...success.')


@factory.django.mute_signals(signals.pre_save)
def create_console_app(apps, schema_editor):
    """
    Create console application.
    If the application already exists, print an error
    """
    username = OAUTH2_APP_OWNER
    user = User.objects.get(username=username)
    model = get_application_model()

    app = model()
    app.user = user
    app.name = OAUTH2_APP_CLIENTS['console']['name']
    app.client_id = OAUTH2_APP_CLIENTS['console']['client_id']
    app.redirect_uris = OAUTH2_APP_CLIENTS['console']['redirect_uris']
    app.client_type = OAUTH2_APP_CLIENTS['console']['client_type']
    app.authorization_grant_type = OAUTH2_APP_CLIENTS[
        'console']['authorization_grant_type']
    app.skip_authorization = OAUTH2_APP_CLIENTS[
        'console']['skip_authorization']

    try:
        app.save()
        print_if_not_testing('...success.')
    except IntegrityError as e:
        print_if_not_testing("...console app not created: " + e.message)


def print_if_not_testing(message):
    if 'test' not in sys.argv:
        print(message)
