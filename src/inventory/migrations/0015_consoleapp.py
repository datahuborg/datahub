# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from oauth2_provider.models import get_application_model
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import signals
import factory


@factory.django.mute_signals(signals.pre_save)
def create_console_oauth(apps, schema_editor):
    foo = User(username="foo", email="foo@mit.edu")
    foo.save()
    model = get_application_model()
    bar = model()
    bar.user = foo
    bar.name = "Console"
    bar.client_id = '7ByJAnXj2jsMFN1REvvUarQjqXjIAU3nmVB661hR'
    bar.redirect_uris = (
            'https://' + settings.DATAHUB_DOMAIN + '/apps/console/\n'
            'http://' + settings.DATAHUB_DOMAIN + '/apps/console/\n'
            'https://web/apps/console/\n'
            'http://web/apps/console/')
    bar.client_type = 'public'
    bar.authorization_grant_type = 'implicit'
    bar.skip_authorization = True
    bar.save()


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_remove_permissions_model'),
        ('oauth2_provider', '__latest__')
    ]

    operations = [
        migrations.RunPython(create_console_oauth)
    ]
