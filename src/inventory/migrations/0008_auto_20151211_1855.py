# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_rename_auth_user_to_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datahublegacyuser',
            name='issuer',
        ),
        migrations.RemoveField(
            model_name='datahublegacyuser',
            name='subject',
        ),
    ]
