# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_rename_users_table'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='DataHubLegacyUser',
        ),
    ]
