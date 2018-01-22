# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0021_license_view'),
    ]

    operations = [
        migrations.AddField(
            model_name='collaborator',
            name='license_id',
            field=models.IntegerField(default=-1),
        ),
    ]
