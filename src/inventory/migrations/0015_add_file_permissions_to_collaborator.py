# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


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
    ]
