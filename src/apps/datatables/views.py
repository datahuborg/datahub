import json
from django.shortcuts import render
from django.http import HttpResponse

from core.db.manager import DataHubManager
from account.auth import *

from models.draw_request import DrawRequest

def error_response():
    return HttpResponse(json.dumps({"success": False}), content_type="application/json")

def json_response(json_dict):
    json_dict["success"] = True
    return HttpResponse(json.dumps(json_dict), content_type="application/json")

def table(request, repo, table):
    print DrawRequest(request)
    return HttpResponse(json.dumps({"success": True}), content_type="application/json")

def get_repos(manager):
    result_set = manager.list_repos()
    if 'tuples' in result_set:
        repos = [t[0] for t in result_set['tuples']]
        return repos
    return None

def get_tables(manager, repo_name):
    result_set = manager.list_tables(repo_name)
    if 'tuples' in result_set:
        tables = [t[0] for t in result_set['tuples']]
        return tables 
    return None

@login_required
def schema(request, repo, table):
    username = get_login(request)
    manager = DataHubManager(username)
    repos = get_repos(manager)
    if repos is not None and repo in repos:
        tables = get_tables(manager, repo)
        if tables is not None and table in tables:
            schema = manager.get_schema(repo + "." + table)
            if schema is not None and 'tuples' in schema:
                return json_response({"schema": schema["tuples"]})
    return error_response()
