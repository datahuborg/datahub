import factory
from django.db.models import signals

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from oauth2_provider.models import get_application_model

from config.settings import OAUTH2_APP_OWNER, \
    OAUTH2_APP_OWNER_EMAIL, \
    OAUTH2_APP_CLIENTS
from core.db.manager import DataHubManager


class Command(BaseCommand):
    help = ("Creates the console OAuth2 application, and the related "
            "user/owner")

    def handle(self, *args, **options):
        print('Creating the OAuth2 App Owner...')
        create_oauth2_user(None, None)
        print('Creating the Console Application...')
        create_console_app(None, None)


@factory.django.mute_signals(signals.pre_save)
def create_oauth2_user(apps, schema_editor):
    # Create public user
    username = OAUTH2_APP_OWNER
    email = OAUTH2_APP_OWNER_EMAIL
    password = None
    users = User.objects.filter(username=username)

    dh_user_exists = bool(len(users) > 0)
    db_exists = DataHubManager.database_exists(username)
    db_role_exists = DataHubManager.user_exists(username)
    user_data_folder_exists = DataHubManager.user_data_folder_exists(username)

    # try to create the django user. Get the password from them
    if not dh_user_exists:
        User.objects.create_user(
            username=username, email=email, password=password)

    # delete any db that exists
    if db_exists:
        DataHubManager.remove_database(
            repo_base=username, revoke_collaborators=True)

    # delete any db role that exists
    if db_role_exists:
        DataHubManager.remove_user(username, remove_db=False,
                                   ignore_missing_user=False)

    # delete any user data folder that exists
    if user_data_folder_exists:
        DataHubManager.delete_user_data_folder(username)

    print('...success.')


@factory.django.mute_signals(signals.pre_save)
def create_console_app(apps, schema_editor):
    # Create anonymous user
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
    app.save()

    print('...success.')
