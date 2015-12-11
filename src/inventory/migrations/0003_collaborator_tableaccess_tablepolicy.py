# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20150626_1438'),
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
                ('user', models.ForeignKey(to='inventory.User')),
            ],
            options={
                'db_table': 'collaborators',
            },
        ),
        migrations.CreateModel(
            name='TableAccess',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('repo_name', models.CharField(max_length=50)),
                ('table_name', models.CharField(max_length=50)),
                ('access_status', models.CharField(max_length=50)),
                ('user', models.ForeignKey(to='inventory.User')),
            ],
            options={
                'db_table': 'table_access',
            },
        ),
        migrations.CreateModel(
            name='TablePolicy',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('repo_name', models.CharField(max_length=50)),
                ('table_name', models.CharField(max_length=50)),
                ('policy_type', models.CharField(max_length=50)),
                ('predicates', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'table_policies',
            },
        ),
    ]
