# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_add_django_user_relation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='app',
            old_name='auth_user',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='permission',
            old_name='auth_user',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='app',
            name='legacy_user',
            field=models.ForeignKey(
                to='inventory.DataHubLegacyUser', null=True),
        ),
        migrations.AlterField(
            model_name='permission',
            name='legacy_user',
            field=models.ForeignKey(
                to='inventory.DataHubLegacyUser', null=True),
        ),
    ]
