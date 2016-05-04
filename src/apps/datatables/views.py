import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from core.db.manager import DataHubManager
from util.run_draw_request import RunDrawRequest

from models.draw_request import DrawRequest
from models.draw_response import DrawResponse


def error_response():
    return HttpResponse(json.dumps({"success": False}),
                        content_type="application/json")


def json_response(json_dict):
    json_dict["success"] = True
    return HttpResponse(json.dumps(json_dict),
                        content_type="application/json")


@login_required
def table(request, repo, table):
    username = request.user.get_username()
    manager = DataHubManager(username)
    repos = get_repos(manager)
    if repos is not None and repo in repos:
        tables = get_tables(manager, repo)
        if tables is not None and table in tables:
            draw_request = DrawRequest(request)
            draw_response = RunDrawRequest(
                repo, table, draw_request,
                DrawResponse(draw_request.draw), manager
                ).run()
            return HttpResponse(draw_response.to_json(),
                                content_type="application/json")
    return error_response()


def get_repos(manager):
    repos = manager.list_repos()
    if len(repos) > 0:
        return repos
    return None


def get_tables(manager, repo_name):
    tables = manager.list_tables(repo_name)
    if len(tables) > 0:
        return tables
    return None


@login_required
def schema(request, repo, table):
    username = request.user.get_username()
    manager = DataHubManager(username)
    repos = get_repos(manager)
    if repos is not None and repo in repos:
        tables = get_tables(manager, repo)
        if tables is not None and table in tables:
            schema = manager.get_schema(repo, table)
            if len(schema) > 0:
                return json_response({"schema": schema})
    return error_response()


@login_required
def aggregate(request, repo, table, agg_type, col_name):
    username = request.user.get_username()
    manager = DataHubManager(username)
    repos = get_repos(manager)
    # Ensure that the repo exists.
    if repos is not None and repo in repos:
        tables = get_tables(manager, repo)
        # Ensure that the table exists.
        if tables is not None and table in tables:
            schema = manager.get_schema(repo, table)
            # Ensure that the schema for the repo.table exists.
            if len(schema) > 0:
                for c_name, c_type in schema:
                    if c_name == col_name and can_apply(agg_type, col_name):
                        result = manager.execute_sql(
                            "SELECT %s(%s) FROM %s.%s" % (agg_type.lower(), col_name.lower(), repo, table))
                        if "tuples" in result and len(result["tuples"]) > 0 and len(result["tuples"][0]) > 0:
                            return json_response({"value": result["tuples"][0]})
    return error_response()


def can_apply(agg, col_type):
    number_types = ["bigint", "int8", "bigserial", "serial8", "double precision", "float8",
                    "integer", "int", "int4", "real", "float4", "smallint", "int2", "serial", "serial4"]
    agg = agg.lower()
    if agg == "sum" or agg == "avg":
        return agg in number_types
    return agg in ["min", "max", "count"]
