# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_collaborator'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='collaborator',
            unique_together=set([('repo_name', 'repo_owner', 'user')]),
        ),
    ]
