from django.core.management.base import BaseCommand

from django.contrib.auth.models import User

from core.db.manager import DataHubManager
from inventory.models import DataHubLegacyUser


class Command(BaseCommand):
    help = ("create user_data directories for users who don't have them")

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            username = user.username
            if not DataHubManager.user_data_folder_exists(username):
                DataHubManager.create_user_data_folder(repo_base = username)

        legacy_users = DataHubLegacyUser.objects.all()
        for user in legacy_users:
            username = user.username
            if not DataHubManager.user_data_folder_exists(username):
                DataHubManager.create_user_data_folder(repo_base = username)

        success_message = ('I came. I saw. I conquered.\n'
                           '/user_data directory creation is complete.')
        self.stdout.write(self.style.MIGRATE_SUCCESS(success_message))
