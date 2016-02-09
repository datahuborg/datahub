from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from inventory.models import Collaborator, App
from django.db import transaction
from core.db.manager import DataHubManager
from psycopg2 import OperationalError


class Command(BaseCommand):
    help = ("Ensures Django's Collaborator list reflects reality.")

    user_count = 0
    app_count = 0

    def _sync_repo_collaborators(self, manager, base, repo):
        all_names = manager.list_collaborators(repo)
        all_names = [c.get('username') for c in all_names]
        collaborator_names = [c for c in all_names if c != base]
        collaborator_users = User.objects.filter(
            username__in=collaborator_names)
        collaborator_apps = App.objects.filter(app_id__in=collaborator_names)
        for c in collaborator_users:
            _, created = Collaborator.objects.get_or_create(
                user=c, repo_name=repo, repo_base=base,
                defaults={'permission': "ALL"})
            if created:
                self.user_count += 1
                print('User -> {base}.{repo}/{collaborator}'.format(
                    base=base, repo=repo, collaborator=c))
        for c in collaborator_apps:
            _, created = Collaborator.objects.get_or_create(
                app=c, repo_name=repo, repo_base=base,
                defaults={'permission': "ALL"})
            if created:
                self.app_count += 1
                print('App -> {base}.{repo}/{collaborator}'.format(
                    base=base, repo=repo, collaborator=c))

    def handle(self, *args, **options):
        # Throw out all of these changes if it fails somehow
        with transaction.atomic():
            for base in (user.get_username() for user in User.objects.all()):
                try:
                    manager = DataHubManager(user=base, repo_base=base)
                except OperationalError as e:
                    print(e)
                    continue
                repos = manager.list_repos()
                for repo in repos:
                    self._sync_repo_collaborators(manager, base, repo)
            print("Added missing {0} users, {1} missing apps.".format(
                self.user_count, self.app_count))
