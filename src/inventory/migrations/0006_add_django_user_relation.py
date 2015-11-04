# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0005_rename_user_model'),
    ]

    operations = [
        migrations.RenameField(
            model_name='app',
            old_name='user',
            new_name='legacy_user',
        ),
        migrations.RenameField(
            model_name='permission',
            old_name='user',
            new_name='legacy_user',
        ),
        migrations.AddField(
            model_name='app',
            name='auth_user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='permission',
            name='auth_user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
