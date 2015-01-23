import json
from django.shortcuts import render
from django.http import HttpResponse

from core.db.manager import DataHubManager
from account.auth import *

'''
Returns a successful JSON response.

@param json_dict - A dictionary representing the JSON to be sent to the user. It will be augmented
                    with the property, json_dict.success = true

@return An HttpResponse representing the json_dict (augmented with the "success" property).
'''
def json_response(json_dict):
    json_dict["success"] = True
    return HttpResponse(json.dumps(json_dict), content_type="application/json")

'''
Returns a failure JSON response.

@return An HttpResponse representing the JSON object
{
    "success": false
}
'''
def error_response():
    return HttpResponse(json.dumps({"success": False}), content_type="application/json")

'''
Return the repos associated with this user.

@param manager - A DataHubManager object associated with the current user.

@return a list of the repo names associated with the current user, or None if there is an error.
'''
def get_repos(manager):
    result_set = manager.list_repos()
    if 'tuples' in result_set:
        repos = [t[0] for t in result_set['tuples']]
        return repos
    return None

'''
Return the tables in a repo associated with this user.

@param manager - A DataHubManager object associated with the current user.
@param repo_name - The name of the repo, the user must be associated with this repo.

@return a list of the tables in the repo with name = repo_name.
'''
def get_tables(manager, repo_name):
    result_set = manager.list_tables(repo_name)
    if 'tuples' in result_set:
        tables = [t[0] for t in result_set['tuples']]
        return tables 
    return None

'''
Return the list of repos associated with the current user. If successful, the response is JSON of 
the form:

{
    "success": true,
    "repos": [String]
}

If there was a failure, the response is JSON of the form:

{
    "success": false
}
'''
@login_required
def repos(request):
    username = get_login(request)
    manager = DataHubManager(username)
    repos = get_repos(manager)
    if repos is not None:
        return json_response({"repos": repos})
    return error_response()

'''
Return the list of tables in the repo associated with the current user. 
If successful, the response is JSON of the form:

{
    "success": true,
    "tables": [String]
}

If there was a failure, the response is JSON of the form:

{
    "success": false
}
'''
@login_required
def tables(request, repo_name):
    username = get_login(request)
    manager = DataHubManager(username)
    repos = get_repos(manager)
    if repos is not None and repo_name in repos:
        tables = get_tables(manager, repo_name)
        if tables is not None:
            return json_response({"tables": tables})
    return error_response()

'''
Return the schema for the table in the given repo associated with the current user. 
If successful, the response is JSON of the form:

{
    "success": true,
    "schema": [[<field_name>String, <field_type>String]]
}

If there was a failure, the response is JSON of the form:

{
    "success": false
}
'''
@login_required
def schema(request, repo_name, table_name):
    username = get_login(request)
    manager = DataHubManager(username)
    repos = get_repos(manager)
    if repos is not None and repo_name in repos:
        tables = get_tables(manager, repo_name)
        if tables is not None and table_name in tables:
            schema = manager.get_schema(repo_name + "." + table_name)
            if schema is not None and 'tuples' in schema:
                return json_response({"schema": schema["tuples"]})
    return error_response()
