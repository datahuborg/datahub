from django.core.management.base import BaseCommand, CommandError
from django.utils.crypto import get_random_string
import os.path
from django.conf import settings


class Command(BaseCommand):
    help = 'Generates a new SECRET_KEY at src/config/secret_key.py.'

    def handle(self, *args, **options):
        # Same generator used by Django's startproject command.
        # https://github.com/django/django/blob/stable/1.8.x/django/core/management/commands/startproject.py
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = get_random_string(50, chars)
        path = os.path.join(settings.SETTINGS_DIR, 'secret_key.py')
        try:
            with open(path, 'w') as file:
                file.write("SECRET_KEY = '{0}'\n".format(key))
        except Exception, e:
            raise CommandError(e)
