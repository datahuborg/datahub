import factory

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.db.manager import DataHubManager
from django.db.models import signals
from django.db import transaction

from config import settings
from core.db.backend.pg import PGBackend
from inventory.models import *


class Command(BaseCommand):
    help = ("Migrates from DataHub's old custom user model to the new model "
            "based on Django's default User model.")

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            dest='force',
            default=False,
            help="Migrate accounts even if some users "
                 "are already using the new model.")

    def handle(self, *args, **options):
        migrate_datahub_accounts()


# Disable pre_save signals that would otherwise cancel user creation
# because we're creating users for usernames that already have db roles.
# Also, we don't want to create a database for these users since those
# already exist as well.
#
# @factory comes from the factory_boy module.


@factory.django.mute_signals(signals.pre_save)
def migrate_datahub_accounts(*args, **kwargs):
    old_users = DataHubLegacyUser.objects.all()
    apps = App.objects.exclude(legacy_user=None)
    users = User.objects.all()
    print("Old model users: {0} New model users: {1}".format(
        len(old_users), len(users)))
    print("Apps: {0}".format(len(apps)))

    new_users = []
    # Throw out all of these changes if it fails somehow
    with transaction.atomic():
        for old_user in old_users:
            try:
                User.objects.get(username=old_user.username)
            except User.DoesNotExist:
                new_user = User.objects.create_user(
                    username=old_user.username,
                    email=old_user.email)
                new_users.append(new_user)
            DataHubManager.create_user_data_folder(
                repo_base=old_user.username)

        for app in apps:
            username = app.legacy_user.username
            print("{0} legacy_user is {1}".format(
                app.app_id,
                username))
            if app.user is None:
                new_user = User.objects.get(username=username)
                app.user = new_user
                app.save(update_fields=['user'])
            print("    user is {0}".format(app.user.username))

    print("Migrated Users: {0}".format(new_users))

    # grant existing users access to the dh_public role,
    # which is used to share select-only repos
    superuser_username = settings.DATABASES['default']['USER']
    superuser_password = settings.DATABASES['default']['PASSWORD']

    users = User.objects.exclude(username__in=[settings.PUBLIC_ROLE,
                                 settings.OAUTH2_APP_OWNER])
    pg = PGBackend(superuser_username, superuser_password)

    for user in users:
        query = 'GRANT %s to %s' % (settings.PUBLIC_ROLE, user.username)
        print(query)
        try:
            pg.execute_sql(query)
        except ValueError:
            print('Skipped %s due to missing role.' % user.username)
            pass
    pg.close_connection()

    print 'grants complete'
