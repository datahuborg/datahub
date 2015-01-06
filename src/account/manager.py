import hashlib
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from core.db.manager import DataHubManager
from inventory.models import *


'''
@author: Anant Bhardwaj
@date: Feb 12, 2012
'''


def account_login (username, email, password):
  hashed_password = hashlib.sha1(password).hexdigest()
  if username:
    return User.objects.get(username=username, password=hashed_password)
  else:
    return User.objects.get(email=email, password=hashed_password)

def account_register (username, email, password, app_id, app_token):
  if not app_id:
    raise Exception("Invalid app_id")

  if not app_token:
    raise Exception("Invalid app_token")

  app = None
  try:
    app = App.objects.get(app_id=app_id)
  except App.DoesNotExist:
    raise Exception("Invalid app_id")
  
  if app.app_token != app_token:
    raise Exception("Invalid app_token")
  
  hashed_password = hashlib.sha1(password).hexdigest()
  user = User(username=username, email=email, password=hashed_password)
  user.save()
  try:
    DataHubManager.create_user(username=username, password=hashed_password)
  except Exception, e:
    user.delete()
    raise e

  return user

def account_remove (username, app_id, app_token):
  if not app_id:
    raise Exception("Invalid app_id")

  if not app_token:
    raise Exception("Invalid app_token")

  app = None
  try:
    app = App.objects.get(app_id=app_id)
  except App.DoesNotExist:
    raise Exception("Invalid app_id")
  
  if app.app_token != app_token:
    raise Exception("Invalid app_token")
  
  app = App.objects.get(app_id=app_id)
  
  if app.app_token != app_token:
    raise Exception("Incorrect app token")
  
  user = User.objects.get(username=username)
  user.delete()  
  DataHubManager.remove_user(username=username)
