import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")



PROJECT_ROOT = os.path.dirname(__file__)+"/../"
path = os.path.join(PROJECT_ROOT, 'apps')
sys.path.append(path)
path = os.path.join(PROJECT_ROOT, 'gen-py')
sys.path.append(path)

def before_all(context):
    from django.test import Client
    django.setup()
    context.client = Client()

def before_scenario(context, scenario):
    pass


def after_scenario(context, scenario):
    pass
