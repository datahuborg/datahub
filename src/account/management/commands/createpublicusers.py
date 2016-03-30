from config import settings

from django.utils.crypto import get_random_string
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from core.db.manager import DataHubManager


class Command(BaseCommand):
    help = ("Creates the default datahub public and anonomous users "
            "that public repos will be shared with.")

    def handle(self, *args, **options):

        self.create_public_user()
        self.create_anonomous_user()

    def create_public_user(self):
        # Create public user
        username = settings.PUBLIC_ROLE
        email = settings.PUBLIC_ROLE_EMAIL
        # generate a password for the public user
        # This will never be used, so the original passowrd is not stored.
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
        password = get_random_string(10, chars)

        users = User.objects.filter(username=username)

        if len(users) > 0:
            print('\n==> public user already created. Not creating public user\n')
            return

        try:
            message = (
                '\n==>creating public user %s with email %s '
                'and password %s \n') % (username, email, password)
            print message
            User.objects.create_user(
                username=username, email=email,
                password=password)
        except Exception as e:
            print '\n==>failed to create public user.'
            print e.message

    def create_anonomous_user(self):
        # Create anonomous user
        username = settings.ANONOMOUS_ROLE
        email = settings.ANONOMOUS_ROLE_EMAIL
        # generate a password for the public user
        # This will never be used, so the original passowrd is not stored.
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
        password = get_random_string(10, chars)

        users = User.objects.filter(username=username)

        if len(users) > 0:
            print(
                '\n==> anonomous user already created. '
                'Not creating anonomous user\n')
            return

        try:
            # create the user
            message = (
                '\n==> creating anonomous user %s with email %s '
                'and password %s \n') % (username, email, password)
            print message
            User.objects.create_user(
                username=username, email=email,
                password=password)

            # Immediately remove the associated db and user file directory.
            # (It's easier to create and then delete, since there's no
            # knowing what future create user signals will do.)
            message = (
                '\n==>removing anonomous user %s database.\n' % (username))
            print message
            DataHubManager.remove_database(username)

        except Exception as e:
            print '\n==>failed to create anonomous user.'
            print e.message
