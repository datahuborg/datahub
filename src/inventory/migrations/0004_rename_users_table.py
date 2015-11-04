# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_merge'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='user',
            table='datahub_legacy_users',
        ),
    ]
