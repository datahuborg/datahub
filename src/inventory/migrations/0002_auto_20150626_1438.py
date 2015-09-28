# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comments',
        ),
        migrations.RemoveField(
            model_name='dashboardcard',
            name='card',
        ),
        migrations.RemoveField(
            model_name='dashboardcard',
            name='dashboard',
        ),
        migrations.DeleteModel(
            name='Dashboard',
        ),
        migrations.DeleteModel(
            name='DashboardCard',
        ),
    ]
