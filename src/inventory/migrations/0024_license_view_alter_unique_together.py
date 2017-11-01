# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0023_auto_20170831_1614'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='licenseview',
            unique_together=set(
                [('repo_name', 'repo_base', 'table', 'license_id')]),
        ),
    ]
