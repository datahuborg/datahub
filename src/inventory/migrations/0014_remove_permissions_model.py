# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_add_app_to_collaborator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permission',
            name='app',
        ),
        migrations.RemoveField(
            model_name='permission',
            name='legacy_user',
        ),
        migrations.RemoveField(
            model_name='permission',
            name='user',
        ),
        migrations.DeleteModel(
            name='Permission',
        ),
    ]
