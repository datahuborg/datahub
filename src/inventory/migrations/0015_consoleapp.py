# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from account.management.commands.createoauthappsandowner import(
    create_oauth2_user, create_console_app)


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_remove_permissions_model'),
        ('oauth2_provider', '__latest__')
    ]

    operations = [
        migrations.RunPython(create_oauth2_user),
        migrations.RunPython(create_console_app)
    ]
