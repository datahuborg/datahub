import hashlib
import os
from core.db.manager import DataHubManager
from inventory.models import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


'''
@author: Anant Bhardwaj
@date: Feb 12, 2012
'''


def account_login(username, email, password):
    hashed_password = hashlib.sha1(password).hexdigest()
    if username:
        return DataHubLegacyUser.objects.get(username=username, password=hashed_password)
    else:
        return DataHubLegacyUser.objects.get(email=email, password=hashed_password)


def account_register(username, email, password, repo_name, app_id, app_token):
    try:
        user = DataHubLegacyUser.objects.get(username=username)
        raise Exception("Duplicate username (email=%s)" % (user.email))
    except DataHubLegacyUser.DoesNotExist:
        pass

    try:
        user = DataHubLegacyUser.objects.get(email=email)
        raise Exception("Duplicate email (username=%s)" % (user.username))
    except DataHubLegacyUser.DoesNotExist:
        pass

    hashed_password = hashlib.sha1(password).hexdigest()
    user = DataHubLegacyUser(username=username, email=email, password=hashed_password)
    user.save()

    try:
        DataHubManager.create_user(username=username, password=hashed_password)
        account_grant_permission(
            username=username,
            repo_name=repo_name,
            app_id=app_id,
            app_token=app_token)
    except Exception, e:
        user.delete()
        raise e

    return user


def account_grant_permission(username, repo_name, app_id, app_token):
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

    try:
        manager = DataHubManager(user=username)
        manager.create_repo(repo_name)
        manager.add_collaborator(
            repo_name,
            app_id,
            privileges=['SELECT', 'INSERT', 'UPDATE', 'DELETE'])
    except Exception, e:
        raise e


def account_remove(username, app_id, app_token):
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

    DataHubManager.remove_user(username=username)

    user = DataHubLegacyUser.objects.get(username=username)
    user.delete()
