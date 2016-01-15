from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from inventory.models import *
import factory
from django.db.models import signals
from django.db import transaction


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

    # Disable pre_save signals that would otherwise cancel user creation
    # because we're creating users for usernames that already have db roles.
    # Also, we don't want to create a database for these users since those
    # already exist as well.
    #
    # @factory comes from the factory_boy module.
    @factory.django.mute_signals(signals.pre_save)
    def handle(self, *args, **options):
        old_users = DataHubLegacyUser.objects.all()
        apps = App.objects.all()
        users = User.objects.all()
        print("Old model users: {0} New model users: {1}".format(
            len(old_users), len(users)))
        print("Apps: {0}".format(len(apps)))

        if len(users) > 0 and not options['force']:
            print("There are already some users using the new model. "
                  "If this is expected, force migration with --force.")
            return

        new_users = []
        # Throw out all of these changes if it fails somehow
        with transaction.atomic():
            for old_user in old_users:
                try:
                    User.objects.get(username=old_user.username)
                except User.DoesNotExist:
                    new_user = User.objects.create_user(
                        username=old_user.username,
                        email=old_user.email
                        )
                    new_users.append(new_user)

            for app in apps:
                username = app.legacy_user.username
                print("{0} legacy_user is {1}".format(
                    app.app_id,
                    username
                    ))
                if app.user is None:
                    new_user = User.objects.get(username=username)
                    app.user = new_user
                    app.save(update_fields=['user'])
                print("    user is {0}".format(app.user.username))

        print("Migrated Users: {0}".format(new_users))
