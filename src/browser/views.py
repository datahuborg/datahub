import json
import urllib
import uuid
import hashlib

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.core import serializers

from django.http import HttpResponse, \
                        HttpResponseRedirect, \
                        HttpResponseForbidden, \
                        HttpResponseNotAllowed
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt

from thrift.protocol import TBinaryProtocol
from thrift.protocol import TJSONProtocol
from thrift.transport.TTransport import TMemoryBuffer


from config import settings
from oauth2_provider.models import get_application_model
from oauth2_provider.views import ApplicationUpdate
from inventory.models import App, Annotation
from account.utils import grant_app_permission
from core.db.manager import DataHubManager
from datahub import DataHub
from datahub.account import AccountService
from service.handler import DataHubHandler
from utils import post_or_get, custom_manager_error_handler

'''
@author: Anant Bhardwaj
@date: Mar 21, 2013

Datahub Web Handler
'''

handler = DataHubHandler()
core_processor = DataHub.Processor(handler)
account_processor = AccountService.Processor(handler)


def home(request):
    username = request.user.get_username()
    if username:
        return HttpResponseRedirect(reverse('browser-user', args=(username,)))
    else:
        return HttpResponseRedirect(reverse('www:index'))


def about(request):
    return HttpResponseRedirect(reverse('www:index'))


'''
APIs and Services
'''


@csrf_exempt
def service_core_binary(request):
        # Catch CORS preflight requests
    if request.method == 'OPTIONS':
        resp = HttpResponse('')
        resp['Content-Type'] = 'text/plain charset=UTF-8'
        resp['Content-Length'] = 0
        resp.status_code = 204
    else:
        try:
            iprot = TBinaryProtocol.TBinaryProtocol(
                TMemoryBuffer(request.body))
            oprot = TBinaryProtocol.TBinaryProtocol(TMemoryBuffer())
            core_processor.process(iprot, oprot)
            resp = HttpResponse(oprot.trans.getvalue())

        except Exception as e:
            resp = HttpResponse(
                json.dumps({'error': str(e)}),
                content_type="application/json")
    try:
        resp['Access-Control-Allow-Origin'] = request.META['HTTP_ORIGIN']
    except:
        pass
    resp['Access-Control-Allow-Methods'] = "POST, PUT, GET, DELETE, OPTIONS"
    resp['Access-Control-Allow-Credentials'] = "true"
    resp['Access-Control-Allow-Headers'] = ("Authorization, Cache-Control, "
                                            "If-Modified-Since, Content-Type")

    return resp


@csrf_exempt
def service_account_binary(request):
    # Catch CORS preflight requests
    if request.method == 'OPTIONS':
        resp = HttpResponse('')
        resp['Content-Type'] = 'text/plain charset=UTF-8'
        resp['Content-Length'] = 0
        resp.status_code = 204
    else:
        try:
            iprot = TBinaryProtocol.TBinaryProtocol(
                TMemoryBuffer(request.body))
            oprot = TBinaryProtocol.TBinaryProtocol(TMemoryBuffer())
            account_processor.process(iprot, oprot)
            resp = HttpResponse(oprot.trans.getvalue())

        except Exception as e:
            resp = HttpResponse(
                json.dumps({'error': str(e)}),
                content_type="application/json")

    try:
        resp['Access-Control-Allow-Origin'] = request.META['HTTP_ORIGIN']
    except:
        pass
    resp['Access-Control-Allow-Methods'] = "POST, PUT, GET, DELETE, OPTIONS"
    resp['Access-Control-Allow-Credentials'] = "true"
    resp['Access-Control-Allow-Headers'] = ("Authorization, Cache-Control, "
                                            "If-Modified-Since, Content-Type")

    return resp


@csrf_exempt
def service_core_json(request):
    # Catch CORS preflight requests
    if request.method == 'OPTIONS':
        resp = HttpResponse('')
        resp['Content-Type'] = 'text/plain charset=UTF-8'
        resp['Content-Length'] = 0
        resp.status_code = 204
    else:
        try:
            iprot = TJSONProtocol.TJSONProtocol(TMemoryBuffer(request.body))
            oprot = TJSONProtocol.TJSONProtocol(TMemoryBuffer())
            core_processor.process(iprot, oprot)
            resp = HttpResponse(
                oprot.trans.getvalue(),
                content_type="application/json")

        except Exception as e:
            resp = HttpResponse(
                json.dumps({'error': str(e)}),
                content_type="application/json")

    try:
        resp['Access-Control-Allow-Origin'] = request.META['HTTP_ORIGIN']
    except:
        pass
    resp['Access-Control-Allow-Methods'] = "POST, PUT, GET, DELETE, OPTIONS"
    resp['Access-Control-Allow-Credentials'] = "true"
    resp['Access-Control-Allow-Headers'] = ("Authorization, Cache-Control, "
                                            "If-Modified-Since, Content-Type")

    return resp


'''
Repository Base
'''


def public(request):
    """browse public repos. Login not required"""

    username = request.user.get_username()
    public_repos = DataHubManager.list_public_repos()

    # This should really go through the api... like everything else
    # in this file.
    public_repos = serializers.serialize('json', public_repos)

    return render_to_response("public-browse.html", {
        'login': username,
        'repo_base': 'repo_base',
        'repos': [],
        'public_repos': public_repos,
        })


def user(request, repo_base=None):
    username = request.user.get_username()

    if not repo_base:
        repo_base = username

    with custom_manager_error_handler(username, repo_base, repo=None):
        manager = DataHubManager(user=username, repo_base=repo_base)
        repos = manager.list_repos()

    visible_repos = []
    public_role = settings.PUBLIC_ROLE

    for repo in repos:
        collaborators = manager.list_collaborators(repo)
        collaborators = [c.get('username') for c in collaborators]
        collaborators = filter(
            lambda x: x != '' and x != repo_base, collaborators)
        non_public_collaborators = filter(
            lambda x: x != public_role, collaborators)

        visible_repos.append({
            'name': repo,
            'owner': repo_base,
            'public': True if public_role in collaborators else False,
            'collaborators': non_public_collaborators,
        })

    collaborator_repos = manager.list_collaborator_repos()

    return render_to_response("user-browse.html", {
        'login': username,
        'repo_base': repo_base,
        'repos': visible_repos,
        'collaborator_repos': collaborator_repos})


'''
Repository
'''


def repo(request, repo_base, repo):
    '''
    forwards to repo_tables method
    '''
    return HttpResponseRedirect(
        reverse('browser-repo_tables', args=(repo_base, repo)))


def repo_tables(request, repo_base, repo):
    '''
    shows the tables under a repo.
    '''
    username = request.user.get_username()

    # get the base tables and views of the user's repo
    with custom_manager_error_handler(username, repo_base, repo):
        manager = DataHubManager(user=username, repo_base=repo_base)
        base_tables = manager.list_tables(repo)
        views = manager.list_views(repo)

    res = {
        'login': username,
        'repo_base': repo_base,
        'repo': repo,
        'base_tables': base_tables,
        'views': views}

    res.update(csrf(request))
    return render_to_response("repo-browse-tables.html", res)


def repo_files(request, repo_base, repo):
    '''
    shows thee files in a repo
    '''
    username = request.user.get_username()
    with custom_manager_error_handler(username, repo_base, repo):
        manager = DataHubManager(user=username, repo_base=repo_base)
        uploaded_files = manager.list_repo_files(repo)

    res = {
        'login': username,
        'repo_base': repo_base,
        'repo': repo,
        'files': uploaded_files}

    res.update(csrf(request))
    return render_to_response("repo-browse-files.html", res)


def repo_cards(request, repo_base, repo):
    '''
    shows the cards in a repo
    '''
    username = request.user.get_username()
    with custom_manager_error_handler(username, repo_base, repo):
        manager = DataHubManager(user=username, repo_base=repo_base)
        cards = manager.list_repo_cards(repo)

    res = {
        'login': username,
        'repo_base': repo_base,
        'repo': repo,
        'cards': cards}

    res.update(csrf(request))
    return render_to_response("repo-browse-cards.html", res)


@login_required
def repo_create(request, repo_base):
    '''
    creates a repo (POST), or returns a page for creating repos (GET)
    '''
    username = request.user.get_username()
    if username != repo_base:
        message = (
            'Error: Permission Denied. '
            '%s cannot create new repositories in %s.'
            % (username, repo_base)
            )
        return HttpResponseForbidden(message)

    if request.method == 'POST':
        repo = request.POST['repo']
        with custom_manager_error_handler(username, repo_base, repo):
            manager = DataHubManager(user=username, repo_base=repo_base)
            manager.create_repo(repo)
        return HttpResponseRedirect(reverse('browser-user', args=(username,)))

    elif request.method == 'GET':
        res = {'repo_base': repo_base, 'login': username}
        res.update(csrf(request))
        return render_to_response("repo-create.html", res)


@login_required
def repo_delete(request, repo_base, repo):
    '''
    deletes a repo in the current database (repo_base)
    '''
    username = request.user.get_username()
    with custom_manager_error_handler(username, repo_base, repo):
        manager = DataHubManager(user=username, repo_base=repo_base)
        manager.delete_repo(repo=repo, force=True)
    return HttpResponseRedirect(reverse('browser-user-default'))


@login_required
def repo_settings(request, repo_base, repo):
    '''
    returns the settings page for a repo.
    '''
    username = request.user.get_username()

    with custom_manager_error_handler(username, repo_base, repo):
        manager = DataHubManager(user=username, repo_base=repo_base)
        collaborators = manager.list_collaborators(repo)

    # if the public role is in collaborators, note that it's already added
    repo_is_public = False
    for collaborator in collaborators:
        if collaborator['username'] == settings.PUBLIC_ROLE:
            repo_is_public = True

    # remove the current user, public user from the collaborator list
    # collaborators = [c.get('username') for c in collaborators]
    collaborators = filter(
        lambda x: x['username'] != '' and x['username'] != username and
        x['username'] != settings.PUBLIC_ROLE, collaborators)

    public_role = settings.PUBLIC_ROLE

    res = {
        'login': username,
        'repo_base': repo_base,
        'repo': repo,
        'collaborators': collaborators,
        'public_role': public_role,
        'repo_is_public': repo_is_public}
    res.update(csrf(request))

    return render_to_response("repo-settings.html", res)


@login_required
def repo_collaborators_add(request, repo_base, repo):
    '''
    adds a user as a collaborator in a repo
    '''
    username = request.user.get_username()
    collaborator_username = request.POST['collaborator_username']
    db_privileges = request.POST.getlist('db_privileges')
    file_privileges = request.POST.getlist('file_privileges')

    with custom_manager_error_handler(username, repo_base, repo):
        manager = DataHubManager(user=username, repo_base=repo_base)
        manager.add_collaborator(
            repo, collaborator_username,
            db_privileges=db_privileges,
            file_privileges=file_privileges
            )

    return HttpResponseRedirect(
            reverse('browser-repo_settings', args=(repo_base, repo,)))


@login_required
def repo_collaborators_remove(request, repo_base, repo, collaborator_username):
    '''
    removes a user from a repo
    '''
    username = request.user.get_username()

    with custom_manager_error_handler(username, repo_base, repo):
        manager = DataHubManager(user=username, repo_base=repo_base)
        manager.delete_collaborator(repo=repo, collaborator=collaborator_username)

    # if the user is removing someone else, return the repo-settings page.
    # otherwise, return the browse page
    if username == repo_base:
        return HttpResponseRedirect(
                reverse('browser-repo_settings', args=(repo_base, repo,)))
    else:
        return HttpResponseRedirect(reverse('browser-user-default'))


'''
Tables & Views
'''


def table(request, repo_base, repo, table):
    '''
    return a page indicating how many
    '''
    current_page = 1
    if request.POST.get('page'):
        current_page = request.POST.get('page')

    username = request.user.get_username()
    url_path = reverse('browser-table', args=(repo_base, repo, table))

    with custom_manager_error_handler(username, repo_base, repo):
        manager = DataHubManager(user=username, repo_base=repo_base)
        query = manager.select_table_query(repo, table)
        res = manager.paginate_query(
            query=query, current_page=current_page, rows_per_page=50)

    # get annotation to the table:
    annotation, created = Annotation.objects.get_or_create(url_path=url_path)
    annotation_text = annotation.annotation_text

    data = {
        'login': username,
        'repo_base': repo_base,
        'repo': repo,
        'table': table,
        'annotation': annotation_text,
        'current_page': current_page,
        'next_page': current_page + 1,  # the template should relaly do this
        'prev_page': current_page - 1,  # the template should relaly do this
        'url_path': url_path,
        'column_names': res['column_names'],
        'tuples': res['rows'],
        'total_pages': res['total_pages'],
        'pages': range(res['start_page'], res['end_page'] + 1),  # template
        'num_rows': res['num_rows'],
        'time_cost': res['time_cost']
    }

    data.update(csrf(request))

    # and then, after everything, hand this off to table-browse. It turns out
    # that this is all using DataTables anyhow, so the template doesn't really
    # use all of the data we prepared. ARC 2016-01-04
    return render_to_response("table-browse.html", data)


@login_required
def table_export(request, repo_base, repo, table_name):
    username = request.user.get_username()

    with custom_manager_error_handler(username, repo_base, repo):
        DataHubManager.export_table(
            username=username, repo_base=repo_base, repo=repo,
            table=table_name, file_format='CSV', delimiter=',', header=True)

    return HttpResponseRedirect(
        reverse('browser-repo_files', args=(repo_base, repo)))


@login_required
def table_delete(request, repo_base, repo, table_name):
    """
    Deletes the given table.

    Does not currently allow the user the option to cascade in the case of
    dependencies, though the delete_table method does allow cascade (force) to
    be passed.
    """
    username = request.user.get_username()

    with custom_manager_error_handler(username, repo_base, repo):
        manager = DataHubManager(user=username, repo_base=repo_base)
        manager.delete_table(repo, table_name)

    return HttpResponseRedirect(
        reverse('browser-repo_tables', args=(repo_base, repo)))


@login_required
def view_delete(request, repo_base, repo, view_name):
    """
    Deletes the given view.

    Does not currently allow the user the option to cascade in the case of
    dependencies, though the delete_table method does allow cascade (force) to
    be passed.
    """
    username = request.user.get_username()

    with custom_manager_error_handler(username, repo_base, repo):
        manager = DataHubManager(user=username, repo_base=repo_base)
        manager.delete_view(repo, view_name)

    return HttpResponseRedirect(
        reverse('browser-repo_tables', args=(repo_base, repo)))

'''
Files
'''


@login_required
def file_upload(request, repo_base, repo):
    username = request.user.get_username()
    data_file = request.FILES['data_file']

    with custom_manager_error_handler(username, repo_base, repo):
        manager = DataHubManager(username, repo_base)
        manager.save_file(repo, data_file)

    return HttpResponseRedirect(
        reverse('browser-repo_files', args=(repo_base, repo)))


@login_required
def file_import(request, repo_base, repo, file_name):
    username = request.user.get_username()
    delimiter = str(request.GET['delimiter'])

    if delimiter == '':
        delimiter = str(request.GET['other_delimiter'])

    header = False
    if request.GET['has_header'] == 'true':
        header = True

    quote_character = request.GET['quote_character']
    if quote_character == '':
        quote_character = request.GET['other_quote_character']

    with custom_manager_error_handler(username, repo_base, repo):
        DataHubManager.import_file(
            username=username,
            repo_base=repo_base,
            repo=repo,
            table=table,
            file_name=file_name,
            delimiter=delimiter,
            header=header,
            quote_character=quote_character)

    return HttpResponseRedirect(
        reverse('browser-repo', args=(repo_base, repo)))


@login_required
def file_delete(request, repo_base, repo, file_name):
    username = request.user.get_username()

    with custom_manager_error_handler(username, repo_base, repo):
        manager = DataHubManager(username, repo_base)
        manager.delete_file(repo, file_name)

    return HttpResponseRedirect(
        reverse('browser-repo_files', args=(repo_base, repo)))


def file_download(request, repo_base, repo, file_name):
    username = request.user.get_username()

    with custom_manager_error_handler(username, repo_base, repo):
        manager = DataHubManager(username, repo_base)
        file_to_download = manager.get_file(repo, file_name)

    response = HttpResponse(file_to_download,
                            content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="%s"' % (file_name)
    return response


'''
Query
'''


def query(request, repo_base, repo):
    query = post_or_get(request, key='q', fallback=None)
    username = request.user.get_username()

    # if the user is just requesting the query page
    if not query:
        data = {
            'login': username,
            'repo_base': repo_base,
            'repo': repo,
            'select_query': False,
            'query': None}
        return render_to_response("query.html", data)

    # if the user is actually executing a query
    current_page = 1
    if request.POST.get('page'):
        current_page = request.POST.get('page')

    url_path = reverse('browser-query', args=(repo_base, repo))

    with custom_manager_error_handler(username, repo_base, repo):
        manager = DataHubManager(user=username, repo_base=repo_base)

        if repo:
            manager.set_search_paths([repo])
        res = manager.paginate_query(
            query=query, current_page=current_page, rows_per_page=50)

    # get annotation to the table:
    annotation, created = Annotation.objects.get_or_create(url_path=url_path)
    annotation_text = annotation.annotation_text

    data = {
        'login': username,
        'repo_base': repo_base,
        'repo': repo,
        'annotation': annotation_text,
        'current_page': current_page,
        'next_page': current_page + 1,  # the template should relaly do this
        'prev_page': current_page - 1,  # the template should relaly do this
        'url_path': url_path,
        'query': query,
        'select_query': res['select_query'],
        'column_names': res['column_names'],
        'tuples': res['rows'],
        'total_pages': res['total_pages'],
        'pages': range(res['start_page'], res['end_page'] + 1),  # template
        'num_rows': res['num_rows'],
        'time_cost': res['time_cost']
    }
    data.update(csrf(request))

    return render_to_response("query-browse-results.html", data)


'''
Annotations
'''


@login_required
def create_annotation(request):
    url = request.POST['url']

    annotation, created = Annotation.objects.get_or_create(url_path=url)
    annotation.annotation_text = request.POST['annotation']
    annotation.save()
    return HttpResponseRedirect(url)


'''
Cards
'''


def card(request, repo_base, repo, card_name):
    username = request.user.get_username()

    # if the user is actually executing a query
    current_page = 1
    if request.POST.get('page'):
        current_page = request.POST.get('page')

    url_path = reverse('browser-query', args=(repo_base, repo))

    with custom_manager_error_handler(username, repo_base, repo):
        manager = DataHubManager(user=username, repo_base=repo_base)
        card = manager.get_card(repo=repo, card_name=card_name)
        res = manager.paginate_query(
            query=card.query, current_page=current_page, rows_per_page=50)

    # get annotation to the table:
    annotation, created = Annotation.objects.get_or_create(url_path=url_path)
    annotation_text = annotation.annotation_text

    data = {
        'login': username,
        'repo_base': repo_base,
        'repo': repo,
        'annotation': annotation_text,
        'current_page': current_page,
        'next_page': current_page + 1,  # the template should relaly do this
        'prev_page': current_page - 1,  # the template should relaly do this
        'url_path': url_path,
        'query': card.query,
        'select_query': res['select_query'],
        'column_names': res['column_names'],
        'tuples': res['rows'],
        'total_pages': res['total_pages'],
        'pages': range(res['start_page'], res['end_page'] + 1),  # template
        'num_rows': res['num_rows'],
        'time_cost': res['time_cost']
    }

    data.update(csrf(request))
    return render_to_response("card-browse.html", data)


@login_required
def card_create(request, repo_base, repo):
    username = request.user.get_username()
    card_name = request.POST['card-name']
    query = request.POST['query']
    url = reverse('browser-card', args=(repo_base, repo, card_name))

    with custom_manager_error_handler(username, repo_base, repo):
        manager = DataHubManager(username, repo_base)
        manager.create_card(repo, query, card_name)

    return HttpResponseRedirect(url)


@login_required
def card_export(request, repo_base, repo, card_name):
    username = request.user.get_username()

    with custom_manager_error_handler(username, repo_base, repo):
        manager = DataHubManager(username, repo_base)
        manager.export_card(repo, card_name)

    return HttpResponseRedirect(
        reverse('browser-repo_files', args=(repo_base, repo)))


@login_required
def card_delete(request, repo_base, repo, card_name):
    username = request.user.get_username()

    with custom_manager_error_handler(username, repo_base, repo):
        manager = DataHubManager(username, repo_base)
        manager.delete_card(repo, card_name)

    return HttpResponseRedirect(
        reverse('browser-repo_cards', args=(repo_base, repo)))


'''
Developer Apps
'''


@login_required
def apps(request):
    username = request.user.get_username()
    user = User.objects.get(username=username)
    thrift_apps = App.objects.filter(user=user)
    oauth_apps = get_application_model().objects.filter(user=request.user)

    c = {
        'login': username,
        'thrift_apps': thrift_apps,
        'oauth_apps': oauth_apps}
    return render_to_response('apps.html', c)


@login_required
def thrift_app_detail(request, app_id):
    username = request.user.get_username()
    user = User.objects.get(username=username)
    app = App.objects.get(user=user, app_id=app_id)
    c = RequestContext(request, {
        'login': request.user.get_username(),
        'app': app
        })
    return render_to_response('thrift_app_detail.html', c)


@login_required
def app_register(request):
    username = request.user.get_username()

    if request.method == "POST":
        try:
            user = User.objects.get(username=username)
            app_id = request.POST["app-id"].lower()
            app_name = request.POST["app-name"]
            app_token = str(uuid.uuid4())
            app = App(
                app_id=app_id, app_name=app_name,
                user=user, app_token=app_token)
            app.save()

            try:
                hashed_password = hashlib.sha1(app_token).hexdigest()
                DataHubManager.create_user(
                    username=app_id, password=hashed_password, create_db=False)
            except Exception as e:
                app.delete()
                raise e

            return HttpResponseRedirect('/developer/apps')
        except Exception as e:
            c = {
                'login': username,
                'errors': [str(e)]}
            c.update(csrf(request))
            return render_to_response('app-create.html', c)
    else:
        c = {'login': username}
        c.update(csrf(request))
        return render_to_response('app-create.html', c)


@login_required
def app_remove(request, app_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        DataHubManager.remove_app(app_id=app_id)
        return HttpResponseRedirect(reverse('browser-apps'))
    except Exception as e:
        c = {'errors': [str(e)]}
        c.update(csrf(request))
        return render_to_response('apps.html', c)


@login_required
def app_allow_access(request, app_id, repo_name):
    username = request.user.get_username()
    try:
        app = None
        try:
            app = App.objects.get(app_id=app_id)
        except App.DoesNotExist:
            raise Exception("Invalid app_id")

        app = App.objects.get(app_id=app_id)

        redirect_url = post_or_get(request, key='redirect_url', fallback=None)

        if request.method == "POST":

            access_val = request.POST['access_val']

            if access_val == 'allow':
                grant_app_permission(
                    username=username,
                    repo_name=repo_name,
                    app_id=app_id,
                    app_token=app.app_token)

            if redirect_url:
                redirect_url = redirect_url + \
                    urllib.unquote_plus('?auth_user=%s' % (username))
                return HttpResponseRedirect(redirect_url)
            else:
                if access_val == 'allow':
                    return HttpResponseRedirect(
                        '/settings/%s/%s' % (username, repo_name))
                else:
                    res = {
                        'msg_title': "Access Request",
                        'msg_body':
                            "Permission denied to the app {0}.".format(app_id)
                    }
                    return render_to_response('confirmation.html', res)
        else:
            res = {
                'login': username,
                'repo_name': repo_name,
                'app_id': app_id,
                'app_name': app.app_name}

            if redirect_url:
                res['redirect_url'] = redirect_url

            res.update(csrf(request))
            return render_to_response('app-allow-access.html', res)
    except Exception as e:
        return HttpResponse(
            json.dumps(
                {'error': str(e)}),
            content_type="application/json")


class OAuthAppUpdate(ApplicationUpdate):
    """
    Customized form for updating a Django OAuth Toolkit client app.

    Reorders some fields and ignores modifications to other fields.

    Extends https://github.com/evonove/django-oauth-toolkit/blob/master/
        oauth2_provider/views/application.py
    """

    fields = ['name', 'client_id', 'client_secret', 'client_type',
              'authorization_grant_type', 'redirect_uris']

    def form_valid(self, form):
        # Make sure registrants can't disable the authorization step.
        # Only site admins can do that.
        original_object = get_application_model().objects.get(
            name=form.instance.name)
        form.instance.skip_authorization = original_object.skip_authorization
        return super(OAuthAppUpdate, self).form_valid(form)
