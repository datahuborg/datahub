# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from django.utils.crypto import get_random_string
from django.contrib.auth.models import User

from config import settings
from core.db.manager import DataHubManager


def create_public_user(apps, schema_editor):
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


def create_anonymous_user(apps, schema_editor):
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


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_remove_permissions_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='collaborator',
            name='file_permission',
            field=models.TextField(default='read write'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='card',
            name='public',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(create_public_user, create_anonymous_user)
    ]
