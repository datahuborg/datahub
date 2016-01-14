# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_auto_20151211_1855'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='card',
            unique_together=set([('repo_base', 'repo_name', 'card_name')]),
        ),
    ]
