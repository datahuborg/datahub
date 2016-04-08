# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from inventory.create_public_anon_users import (
    create_public_user, create_anonymous_user)


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
        migrations.RunPython(create_public_user),
        migrations.RunPython(create_anonymous_user)
    ]
