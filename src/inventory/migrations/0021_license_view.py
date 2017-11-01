# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0020_migrate_bad_card_names'),
    ]

    operations = [
        migrations.CreateModel(
            name='LicenseView',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('view_sql', models.TextField()),
                ('repo_name', models.TextField()),
                ('repo_base', models.TextField()),
                ('table', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('license_id', models.IntegerField()),
            ],
            options={
                'db_table': 'license_views',
            },
        ),
    ]
