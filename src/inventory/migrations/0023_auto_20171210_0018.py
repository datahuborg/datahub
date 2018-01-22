# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0022_add_license_id_to_collaborator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='licenseview',
            name='timestamp',
        ),
        migrations.AlterField(
            model_name='licenseview',
            name='end_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='licenseview',
            name='start_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
