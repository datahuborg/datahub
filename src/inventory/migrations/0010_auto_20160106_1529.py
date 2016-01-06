# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_auto_20160106_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterUniqueTogether(
            name='card',
            unique_together=set([('repo_base', 'repo_name', 'card_name')]),
        ),
    ]
