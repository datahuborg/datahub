from config import settings

from django.utils.crypto import get_random_string
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = ("Creates the default datahub public user "
            "that public repos will be shared with.")

    def handle(self, *args, **options):
        username = settings.PUBLIC_ROLE
        email = settings.PUBLIC_ROLE_EMAIL
        # generate a password for the public user
        # This will never be used, so the original passowrd is not stored.
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
        password = get_random_string(10, chars)

        users = User.objects.filter(username=username)

        if len(users) < 1:
            try:
                message = (
                    'creating public user %s with email %s '
                    'and password %s') % (username, email, password)
                print message
                User.objects.create_user(
                    username=username, email=email,
                    password=password)
            except Exception as e:
                print 'failed to create public user.'
                print e.message
