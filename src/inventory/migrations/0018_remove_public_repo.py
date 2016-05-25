# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from core.management.commands.move_public_schemas_to_default import(
    migrate_tables_and_views)


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0017_security_policy_table')
    ]

    operations = [
        migrations.RunPython(migrate_tables_and_views)
    ]
