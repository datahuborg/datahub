# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0015_add_file_permissions_to_collaborator'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
