# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_auto_20151211_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_name',
            field=models.CharField(unique=True, max_length=50),
        ),
    ]
