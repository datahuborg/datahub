# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('url_path', models.CharField(unique=True, max_length=500)),
                ('annotation_text', models.TextField()),
            ],
            options={
                'db_table': 'annotations',
            },
        ),
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('app_id', models.CharField(unique=True, max_length=100)),
                ('app_name', models.CharField(max_length=100)),
                ('app_token', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'apps',
            },
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('repo_base', models.CharField(max_length=50)),
                ('repo_name', models.CharField(max_length=50)),
                ('card_name', models.CharField(max_length=50)),
                ('query', models.TextField()),
            ],
            options={
                'db_table': 'cards',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('url_path', models.CharField(max_length=500)),
                ('comment', models.TextField()),
            ],
            options={
                'db_table': 'comments',
            },
        ),
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('url_path', models.CharField(unique=True, max_length=200)),
                ('repo_base', models.CharField(max_length=50)),
                ('repo_name', models.CharField(max_length=50)),
                ('dashboard_name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'dashboards',
            },
        ),
        migrations.CreateModel(
            name='DashboardCard',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('card', models.ForeignKey(to='inventory.Card')),
                ('dashboard', models.ForeignKey(to='inventory.Dashboard')),
            ],
            options={
                'db_table': 'dashboard_cards',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('access', models.BooleanField(default=False)),
                ('app', models.ForeignKey(to='inventory.App')),
            ],
            options={
                'db_table': 'permissions',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('email', models.CharField(unique=True, max_length=100)),
                ('username', models.CharField(unique=True, max_length=50)),
                ('f_name', models.CharField(max_length=50, null=True)),
                ('l_name', models.CharField(max_length=50, null=True)),
                ('password', models.CharField(max_length=50)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.AddField(
            model_name='permission',
            name='user',
            field=models.ForeignKey(to='inventory.User'),
        ),
        migrations.AddField(
            model_name='app',
            name='user',
            field=models.ForeignKey(to='inventory.User'),
        ),
    ]
