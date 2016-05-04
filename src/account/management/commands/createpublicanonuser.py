import factory
from django.db.models import signals

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from config import settings
from core.db.manager import DataHubManager


class Command(BaseCommand):
    help = ("Creates the public and anonymous users "
            "necessary for publishing data.")

    def handle(self, *args, **options):
        print('Ensuring public user, role, and db exist...')
        print('Ensuring public data folder does not exist...')
        create_public_user(None, None)
        print('Ensuring anonymous user and role exist...')
        print('Ensuring anonymous db and data folder do not exist...')
        create_anonymous_user(None, None)


@factory.django.mute_signals(signals.pre_save)
def create_public_user(apps, schema_editor):
    # Create public user
    username = settings.PUBLIC_ROLE
    email = settings.PUBLIC_ROLE_EMAIL
    users = User.objects.filter(username=username)

    dh_user_exists = False
    if len(users) > 0:
        dh_user_exists = True
    db_exists = DataHubManager.database_exists(username)
    db_role_exists = DataHubManager.user_exists(username)
    user_data_folder_exists = DataHubManager.user_data_folder_exists(username)

    # try to create the django user. Get the password from them
    password = None
    if not dh_user_exists:
        password = User.objects.create_user(
            username=username, email=email, password=None).password

    # try to create the db role
    if not db_role_exists:
        DataHubManager.create_user(
            username=username, password=password, create_db=False)

    # try to create the db
    if not db_exists:
        DataHubManager.create_user_database(
            username=username)

    # delete any user data folder that exists
    if user_data_folder_exists:
        DataHubManager.delete_user_data_folder(username)


@factory.django.mute_signals(signals.pre_save)
def create_anonymous_user(apps, schema_editor):
    # Create anonymous user
    username = settings.ANONYMOUS_ROLE
    email = settings.ANONYMOUS_ROLE_EMAIL
    users = User.objects.filter(username=username)

    dh_user_exists = False
    if len(users) > 0:
        dh_user_exists = True
    db_exists = DataHubManager.database_exists(username)
    db_role_exists = DataHubManager.user_exists(username)
    user_data_folder_exists = DataHubManager.user_data_folder_exists(username)

    # try to create the django user. Get the password from them
    password = None
    if not dh_user_exists:
        password = User.objects.create_user(
            username=username, email=email, password=None).password

    # try to create the db role
    if not db_role_exists:
        DataHubManager.create_user(
            username=username, password=password, create_db=False)

    # delete any db that exists
    if db_exists:
        DataHubManager.remove_database(
            repo_base=username, revoke_collaborators=False)

    # delete any user data folder that exists
    if user_data_folder_exists:
        DataHubManager.delete_user_data_folder(username)
