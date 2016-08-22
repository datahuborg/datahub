# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from account.management.commands.renamecards import \
    rename_cards


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0019_add_users_to_dh_public'),
    ]

    operations = [
        migrations.RunPython(rename_cards)
    ]
