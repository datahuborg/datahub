import factory
from django.db.models import signals

from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User

from config import settings
from core.db.manager import DataHubManager


class Command(BaseCommand):
    help = ("Creates public an anonymous users that are "
            "necessary for publishing data")

    def handle(self, *args, **options):
        create_public_user(None, None)
        create_anonymous_user(None, None)


@factory.django.mute_signals(signals.pre_save)
def create_public_user(apps, schema_editor):
    # Create public user
    username = settings.PUBLIC_ROLE
    email = settings.PUBLIC_ROLE_EMAIL
    # generate a password for the public user
    # This will never be used, so the original passowrd is not stored.
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    password = get_random_string(10, chars)

    users = User.objects.filter(username=username)

    dh_user_exists = False
    if len(users) > 0:
        dh_user_exists = True
    db_exists = DataHubManager.database_exists(username)
    db_role_exists = DataHubManager.user_exists(username)
    user_data_folder_exists = DataHubManager.user_data_folder_exists(username)

    # try to create the db role
    if not db_role_exists:
        print('creating database role %s' % username)
        DataHubManager.create_user(
            username=username, password=password, create_db=False)

    # try to create the db
    if not db_exists:
        print('creating database %s' % username)
        DataHubManager.create_user_database(
            username=username)

    # try to create the user data folder
    if not user_data_folder_exists:
        print('creating data folder for %s' % username)
        DataHubManager.create_user_data_folder(username)

    # try to create the django user
    if not dh_user_exists:
        print('creating django user %s' % username)
        User.objects.create_user(
            username=username, email=email, password=password)


@factory.django.mute_signals(signals.pre_save)
def create_anonymous_user(apps, schema_editor):
    # Create anonymous user
    username = settings.ANONYMOUS_ROLE
    email = settings.ANONYMOUS_ROLE_EMAIL
    # generate a password for the public user
    # This will never be used, so the original passowrd is not stored.
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    password = get_random_string(10, chars)

    users = User.objects.filter(username=username)

    dh_user_exists = False
    if len(users) > 0:
        dh_user_exists = True
    db_exists = DataHubManager.database_exists(username)
    db_role_exists = DataHubManager.user_exists(username)
    user_data_folder_exists = DataHubManager.user_data_folder_exists(username)

    # try to create the db role
    if not db_role_exists:
        print('creating database role %s' % username)
        DataHubManager.create_user(
            username=username, password=password, create_db=False)

    # try to create the django user
    if not dh_user_exists:
        print('creating django user %s' % username)
        User.objects.create_user(
            username=username, email=email, password=password)

    # delete any db that exists
    if db_exists:
        print('deleting database %s' % username)
        DataHubManager.remove_database(
            repo_base=username, revoke_collaborators=False)

    # delete any user data folder that exists
    if user_data_folder_exists:
        print('deleting user data folder for %s' % username)
        DataHubManager.delete_user_data_folder(username)
