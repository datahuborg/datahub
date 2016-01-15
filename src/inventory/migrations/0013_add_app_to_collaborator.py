# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_change_collaborator_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='collaborator',
            name='app',
            field=models.ForeignKey(to='inventory.App', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='collaborator',
            unique_together=set([('repo_name', 'repo_base', 'user', 'app')]),
        ),
        migrations.RemoveField(
            model_name='collaborator',
            name='legacy_user',
        ),
    ]
