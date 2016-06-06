# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from account.management.commands.migratedatahubaccounts import \
    migrate_datahub_accounts


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0018_remove_public_repo'),
    ]

    operations = [
        migrations.RunPython(migrate_datahub_accounts)
    ]
