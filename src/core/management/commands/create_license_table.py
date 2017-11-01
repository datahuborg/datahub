import factory

from django.db.models import signals
from django.core.management.base import BaseCommand

from config import settings
from core.db.manager import DataHubManager
from core.db.licensemanager import LicenseManager


class Command(BaseCommand):
    help = ("Creates the license schema and table "
            "necessary for creating row level security policies.")

    def handle(self, *args, **options):
        print('Creating the license schema')
        create_license_schema(None, None)

        print('Creating the license table')
        create_license_table(None, None)

        print('Creating the license link table')
        create_license_link_table(None, None)


@factory.django.mute_signals(signals.pre_save)
def create_license_schema(apps, schema_editor):
    LicenseManager.create_license_schema()


@factory.django.mute_signals(signals.pre_save)
def create_license_table(apps, schema_editor):
    LicenseManager.create_license_table()


@factory.django.mute_signals(signals.pre_save)
def create_license_link_table(apps, schema_editor):
    LicenseManager.create_license_link_table()
