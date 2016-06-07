# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from core.management.commands.create_security_policy_table import(
    create_policy_schema, create_policy_table,
    add_existing_users_to_security_policy_table)


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0016_public_repos_cards'),
    ]

    operations = [
        migrations.RunPython(create_policy_schema),
        migrations.RunPython(create_policy_table),
        migrations.RunPython(add_existing_users_to_security_policy_table)
    ]
