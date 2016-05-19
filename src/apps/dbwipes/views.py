import json
import traceback
from functools import wraps

from django.views.decorators.http import require_http_methods
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponse, \
                        HttpResponseForbidden, \
                        HttpResponseBadRequest

from core.db.manager import DataHubManager
from summary import Summary, does_cache_exist, create_cache
from util import SummaryEncoder, where_to_sql, create_sql_obj, pick


def returns_json(f):
    @wraps(f)
    def json_returner(*args, **kwargs):
        r = f(*args, **kwargs)
        if not isinstance(r, basestring):
            r = json.dumps(r, cls=SummaryEncoder)
        return HttpResponse(r, content_type='application/json')
    return json_returner


def index(request, repo_base, repo, table):
    """ Main page for dbWipes """
    username = request.user.get_username()
    cache_exists = does_cache_exist(repo_base)

    enable_scorpion = 0
    title = 'DBWipes'

    schema = get_schema(repo, table, username, repo_base)
    # pick the first number as y, and first non y as x
    x = y = ''
    for col, typ in schema.iteritems():
        if typ == 'num':
            y = col
            break

    for col, typ in schema.iteritems():
        if col != y and typ in ('str', 'text'):
            x = col
            break

    if x == '':
        for col, typ in schema.iteritems():
            if col != y:
                x = col

    context = {
        'enableScorpion': enable_scorpion,
        'cacheExists': json.dumps(cache_exists),
        'js': 'summary',
        'study': 0,
        'title': title,
        'db': repo,
        'table': table,
        'username': username,
        'repo': repo,
        'repo_base': repo_base,
        'x': x,
        'y': y
    }

    context.update(csrf(request))
    return render_to_response("index_base.html", context)


@returns_json
def repos(request):
    """ return the repos in the user's database.
        I think this is only used for (disabled) scorpion features.
    """
    username = request.user.get_username()
    repo_base = request.GET.get('username', None)
    manager = DataHubManager(username, repo_base)
    dbnames = manager.list_repos()
    # q = "SELECT datname FROM pg_database where datistemplate = false;"
    # dbnames = [str(row[0]) for row in manager.execute_sql(query=q)['tuples']]
    return {'databases': dbnames}


@returns_json
def tables(request):
    """ Returns the tables in a user's repo.
        I think this is only used for (disabled) scorpion features.
    """
    username = request.user.get_username()
    repo_base = request.GET.get('username', None)
    manager = DataHubManager(username, repo_base)
    repo = request.GET.get('repo')
    tables = manager.list_tables(repo)
    return {'tables': tables}


def get_schema(repo, table, username, repo_base):
    """ gets the schema of a given repo.table in a repo_base """
    manager = DataHubManager(user=username, repo_base=repo_base)
    pairs = manager.get_schema(repo, table)
    schema = {}
    for col, typ in pairs:
        if typ == 'text':
            typ = 'str'
        if 'double' in typ:
            typ = 'num'
        if 'int' in typ:
            typ = 'num'
        if 'date' in typ or 'time' in typ:
            typ = 'time'
        schema[str(col)] = str(typ)
    return schema


@returns_json
def schema(request):
    """ Figure out the repo_base repo.table, and then use get_schema to
        get the schema of that table
    """
    # This is kind of screwey. DBWipes passes
    # the repo_base as "username"
    # the repo as "db"
    # the table as "table"
    username = request.user.get_username()
    repo_base = request.GET.get('username', '')
    table = request.GET.get('table', '')
    repo = request.GET.get('db', '')
    if not table:
        return {}

    ret = {}
    ret['schema'] = get_schema(repo, table, username, repo_base)
    return ret


@returns_json
def api_tuples(request):
    ret = {}
    jsonstr = request.GET.get('json')
    if not jsonstr:
        # print("query: no json string. giving up")
        return ret

    args = json.loads(jsonstr)
    username = request.user.get_username()
    repo_base = args.get('username')
    repo = args.get('db')
    table = args.get('table')
    where = args.get('where', []) or []
    full_tablename = "%s.%s" % (repo, table)

    where, params = where_to_sql(where)
    if where:
        where = 'AND %s' % where
    # print(where)
    # print(params)

    query = ("WITH XXXX as (select count(*) from %s WHERE 1 = 1 %s) "
             "SELECT * FROM %s "
             "WHERE random() <= 50.0 / (select * from XXXX) %s "
             "LIMIT 50")
    query = query % (full_tablename, where, full_tablename, where)
    params = params + params

    manager = DataHubManager(user=username, repo_base=repo_base)
    res = manager.execute_sql(query, params=params)
    rows = res['tuples']
    cols = [field['name'] for field in res['fields']]

    data = [dict(zip(cols, vals)) for vals in rows]
    ret['data'] = data
    ret['schema'] = get_schema(repo, table, username, repo_base)

    # print("%d points returned" % len(ret.get('data', [])))
    return(ret)


@returns_json
def api_query(request):
    ret = {}
    jsonstr = request.GET.get('json', None)
    if not jsonstr:
        # print("query: no json string. giving up")
        return ret

    args = json.loads(jsonstr)
    username = request.user.get_username()
    repo_base = args.get('username')
    repo = args.get('db')
    table = args.get('table')
    args['table'] = "%s.%s" % (repo, table)

    o, params = create_sql_obj(None, args)
    o.limit = 10000
    query = str(o)
    # print(query)
    # print(params)

    if not repo or not table or not query:
        # print("query: no db/table/query. giving up")
        return ret

    manager = DataHubManager(user=username, repo_base=repo_base)
    res = manager.execute_sql(query, params)
    rows = res['tuples']
    cols = pick(res['fields'], 'name')

    data = [dict(zip(cols, vals)) for vals in rows]
    ret['data'] = data
    ret['schema'] = get_schema(repo, table, username, repo_base)

    # print("%d points returned" % len(ret.get('data', [])))
    return ret


@returns_json
def column_distribution(request):
    username = request.user.get_username()
    # repo_base = request.GET.get('repo_base')
    repo_base = request.GET.get('username')
    repo = request.GET.get('db', 'intel')
    tablename = request.GET.get('table', 'readings')
    where = request.GET.get('where', '')
    col = request.GET.get('col')

    # print('-----')
    # print('username: ' + username)
    # print('repo_base: ' + repo_base)
    # print('-----')

    try:
        nbuckets = int(request.GET.get('nbuckets', 100))
    except Exception as e:
        print(e)
        nbuckets = 100

    full_tablename = "%s.%s" % (repo, tablename)

    summary = Summary(
        repo=repo, tablename=full_tablename, username=username,
        repo_base=repo_base, nbuckets=nbuckets, where=where)
    try:
        typ = summary.get_type(col)
        stats = summary.get_col_stats(col, typ)
    except Exception as e:
        traceback.print_exc()
    finally:
        summary.close()

    data = {
        'col': col,
        'type': typ,
        'stats': stats
    }
    context = {"data": data}
    return context


@returns_json
def column_distributions(request):
    username = request.user.get_username()
    repo_base = request.GET.get('repo_base')
    repo = request.GET.get('db', 'intel')
    tablename = request.GET.get('table', 'readings')
    where = request.GET.get('where', '')
    try:
        nbuckets = int(request.GET.get('nbuckets', 100))
    except Exception as e:
        print(e)
        nbuckets = 100

    full_tablename = "%s.%s" % (repo, tablename)
    summary = Summary(repo, full_tablename, username,
                      repo_base=repo_base, nbuckets=nbuckets, where=where)
    # print('where: %s' % where)
    try:
        stats = summary()
    except Exception as e:
        traceback.print_exc()
    finally:
        summary.close()

    data = []
    for col, typ, col_stats in stats:
        data.append({
            'col': col,
            'type': typ,
            'stats': col_stats
        })

    context = {"data": data}
    return context


@require_http_methods(["POST"])
def create_data_cache(request):
    username = request.user.get_username()
    repo_base = request.POST.get('repo_base', None)
    if username != repo_base:
        return HttpResponseForbidden(
            'Only the owner of this repo can create the data cache')

    cache_created = False
    if not does_cache_exist(repo_base):
        cache_created = create_cache(username)

    if cache_created:
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


@returns_json
def scorpion(request):
    # message = ("Could not load scorpionutil. ",
    #            "Maybe scorpion has not been installed?")
    # print >>sys.stderr, message
    return {'status': "error: could not load scorpion"}


@returns_json
def requestid(request):
    return {'error': "Scorpion not installed"}


@returns_json
def api_status(request):
    return {'error': "Scorpion not installed"}
