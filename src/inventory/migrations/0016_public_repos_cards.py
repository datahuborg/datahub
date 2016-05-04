# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from account.management.commands.createpublicanonuser import(
    create_public_user, create_anonymous_user)


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0015_consoleapp'),
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
        migrations.RunPython(create_public_user),
        migrations.RunPython(create_anonymous_user)
    ]
