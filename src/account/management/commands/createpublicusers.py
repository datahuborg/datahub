from config import settings

from django.utils.crypto import get_random_string
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from core.db.manager import DataHubManager


class Command(BaseCommand):
    help = ("Creates the default datahub public and anonymous users "
            "that public repos will be shared with.")

    def handle(self, *args, **options):

        self.create_public_user()
        self.create_anonymous_user()

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
            print('\n==> public user already created.'
                  'Not creating public user\n')
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

    def create_anonymous_user(self):
        # Create anonymous user
        username = settings.ANONYMOUS_ROLE
        email = settings.ANONYMOUS_ROLE_EMAIL
        # generate a password for the public user
        # This will never be used, so the original passowrd is not stored.
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
        password = get_random_string(10, chars)

        users = User.objects.filter(username=username)

        if len(users) > 0:
            print(
                '\n==> anonymous user already created. '
                'Not creating anonymous user\n')
            return

        try:
            # create the user
            message = (
                '\n==> creating anonymous user %s with email %s '
                'and password %s \n') % (username, email, password)
            print message
            User.objects.create_user(
                username=username, email=email,
                password=password)

            # Immediately remove the associated db and user file directory.
            # (It's easier to create and then delete, since there's no
            # knowing what future create user signals will do.)
            message = (
                '\n==>removing anonymous user %s database.\n' % (username))
            print message
            DataHubManager.remove_database(username)

        except Exception as e:
            print '\n==>failed to create anonymous user.'
            print e.message
