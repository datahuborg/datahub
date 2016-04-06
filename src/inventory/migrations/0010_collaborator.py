# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0009_make_card_names_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collaborator',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('repo_name', models.CharField(max_length=50)),
                ('repo_owner', models.CharField(max_length=50)),
                ('permission', models.CharField(max_length=50)),
                ('legacy_user',
                    models.ForeignKey(to='inventory.DataHubLegacyUser',
                                      null=True)),
                ('user',
                    models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                      null=True)),
            ],
            options={
                'db_table': 'collaborators',
            },
        ),
    ]
