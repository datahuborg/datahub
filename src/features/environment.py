import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")



PROJECT_ROOT = os.path.dirname(__file__)+"/../"
path = os.path.join(PROJECT_ROOT, 'apps')
sys.path.append(path)
path = os.path.join(PROJECT_ROOT, 'gen-py')
sys.path.append(path)

def before_all(context):
    from django.core.management import setup_environ
    from config import settings
    from django.test import Client
    
    setup_environ(settings)
    context.client = Client()


def before_scenario(context, scenario):
    pass


def after_scenario(context, scenario):
    pass
