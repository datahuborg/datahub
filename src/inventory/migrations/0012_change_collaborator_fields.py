# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_make_collaborators_unique'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collaborator',
            old_name='repo_owner',
            new_name='repo_base',
        ),
        migrations.AlterField(
            model_name='collaborator',
            name='repo_name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='collaborator',
            name='repo_base',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='collaborator',
            name='permission',
            field=models.TextField(),
        ),
        migrations.AlterUniqueTogether(
            name='collaborator',
            unique_together=set([('repo_name', 'repo_base', 'user')]),
        ),
    ]
