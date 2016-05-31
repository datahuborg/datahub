import ast
import json

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework_csv.renderers import CSVRenderer
from rest_framework.settings import api_settings
from api.permissions import PublicCardPermission, \
    PublicCardAuthentication

from psycopg2 import Error as PGError
from core.db.manager import PermissionDenied
from django.core.exceptions import ValidationError, \
    ObjectDoesNotExist

from config import settings
from .serializer import (
    UserSerializer, RepoSerializer, CollaboratorSerializer,
    TableSerializer, ViewSerializer, FileSerializer, QuerySerializer,
    CardSerializer, RowLevelSecuritySerializer)


class CurrentUser(APIView):
    """
    The current user.

    GET details on current user.
    Accepts: None
    """

    def get(self, request, format=None):
        username = request.user.get_username()
        user = User.objects.get(username=username)

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)


class CurrentUserRepos(APIView):
    """
    The current user's owned repos.

    GET the repos owned by the current user.
    Accepts: None
    """

    def get(self, request, format=None):
        # redirect to another url
        repo_base = request.user.get_username()
        return HttpResponseRedirect(
            reverse('api:repos_specific', args=(repo_base,)))


class Repos(APIView):
    """
    Repos visible to the logged in user.
    """

    def get(self, request, format=None):
        username = request.user.get_username()
        repo_base = username

        serializer = RepoSerializer(username, repo_base, request)
        return Response(serializer.user_accessible_repos())


class Repo(APIView):
    """
    A specific repo of a specific user
    """

    def get(self, request, repo_base, repo_name, format=None):
        """
        Views, tables, collaborators, and files in a repo
        """
        username = request.user.get_username()
        serializer = RepoSerializer(username, repo_base, request)
        return Response(serializer.describe_repo(repo_name),
                        status=status.HTTP_200_OK)

    def delete(self, request, repo_base, repo_name, format=None):
        """
        Delete a repo
        """
        username = request.user.get_username()
        serializer = RepoSerializer(username, repo_base, request)
        serializer.delete_repo(repo_name=repo_name, force=True)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, repo_base, repo_name, format=None):
        """
        Rename a repo
        ---
        parameters:
          - name: new_name
            in: body
            type: string
            description: new name for the repo
            required: true

        consumes:
          - application/json
        produces:
          - application/json


        """
        username = request.user.get_username()
        serializer = RepoSerializer(username, repo_base, request)
        new_repo_name = request.data['new_name']
        serializer.rename_repo(repo=repo_name, new_name=new_repo_name)

        return Response(serializer.describe_repo(new_repo_name),
                        status=status.HTTP_200_OK)


class ReposPublic(APIView):
    """
    Repos that have been made public
    """

    def get(self, request, format=None):
        serializer = RepoSerializer(settings.ANONYMOUS_ROLE, None, request)
        return Response(serializer.public_repos())


class ReposForUser(APIView):
    """
    Repos of the specified user.
    """

    def get(self, request, repo_base, format=None):
        """
        Repos of the specified user that are visible to the logged in user
        """
        username = request.user.get_username()
        serializer = RepoSerializer(username, repo_base, request)

        if username == repo_base:
            return Response(serializer.user_owned_repos())
        else:
            return Response(serializer.specific_collab_repos(repo_base))

    def post(self, request, repo_base, format=None):
        """
        Create a repo for the specified user.
        ---
        omit_serializer: true
        parameters:
          - name: repo_name
            in: body
            type: string
            description: name of the repo to be created
            required: true

        """
        username = request.user.get_username()
        serializer = RepoSerializer(username, repo_base, request)

        repo_name = request.data['repo_name']
        serializer.create_repo(repo_name)

        return Response(serializer.user_accessible_repos(),
                        status=status.HTTP_201_CREATED)


class Collaborators(APIView):
    """
    List and create collaborators.

    GET to list the collaborators.
    Accepts: None
    ---
    POST to add a collaborator.
    Accepts: { "user":, "permissions": []}
    e.g. {"user":"foo_user", "permissions": ['SELECT', 'INSERT', 'UPDATE']}
    """

    def get(self, request, repo_base, repo_name, format=None):
        """
        Collaborators in a repo
        """
        username = request.user.get_username()
        serializer = CollaboratorSerializer(username=username,
                                            repo_base=repo_base,
                                            request=request)
        collaborators = serializer.list_collaborators(repo_name)

        return Response(collaborators, status=status.HTTP_200_OK)

    def post(self, request, repo_base, repo_name, format=None):
        """
        Add a collaborator to a repo
        ---
        omit_serializer: true

        parameters:
          - name: user
            in: body
            type: string
            description: user to be added as a collaborator
            required: true
          - name: db_permissions
            in: body
            type: array
            items: {
              type: string
            }
            required: true
          - name: file_permissions
            in: body
            type: array
            items: {
                type: string
            }
            required: true
        """
        username = request.user.get_username()
        serializer = CollaboratorSerializer(username=username,
                                            repo_base=repo_base)
        data = request.data
        collaborator = data['user']
        db_permissions = str(data['db_permissions'])
        db_permissions = ast.literal_eval(db_permissions)
        file_permissions = str(data['file_permissions'])
        file_permissions = ast.literal_eval(file_permissions)

        serializer.add_collaborator(
            repo_name, collaborator, db_permissions, file_permissions)
        collaborator = serializer.describe_collaborator(
            repo_name, collaborator)

        return Response(collaborator, status=status.HTTP_201_CREATED)


class Collaborator(APIView):
    """
    View, Modify and delete existing collaborators.
    """

    def get(self, request, repo_base, repo_name, collaborator, format=None):
        """
        View collaborator permissions on a given repo
        """
        username = request.user.get_username()
        serializer = CollaboratorSerializer(username=username,
                                            repo_base=repo_base,
                                            request=request)
        collaborators = serializer.describe_collaborator(
            repo_name, collaborator)
        return Response(collaborators, status=status.HTTP_200_OK)

    def delete(self, request, repo_base, repo_name, collaborator, format=None):
        """
        Remove a collaborator from a given repo
        """
        username = request.user.get_username()
        serializer = CollaboratorSerializer(username=username,
                                            repo_base=repo_base)
        serializer.remove_collaborator(repo_name, collaborator)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class Tables(APIView):

    def get(self, request, repo_base, repo_name, format=None):
        """
        Tables in a repo
        """
        username = request.user.get_username()
        serializer = TableSerializer(
            username=username, repo_base=repo_base, request=request)

        tables = serializer.list_tables(repo_name)
        return Response(tables, status=status.HTTP_200_OK)

    def post(self, request, repo_base, repo_name, format=None):
        """
        Create a table in a repo

        note: Using execute_query to create tables gives more control over
        table creation
        e.g. { "table_name": "mytablename",
           "params": [{"column_name":"foo", "data_type":"integer" }]}
        ---
        omit_serializer: true

        parameters:
          - name: table_name
            in: body
            type: string
            description: name of the table to be created
            required: true
          - name: params
            in: body
            schema:
            description: column names and data types in those columns
            type: array[{'column_name': '', 'data_type': ''} ...]
            required: true

        """
        username = request.user.get_username()
        serializer = TableSerializer(
            username=username, repo_base=repo_base)

        table_name = request.data['table_name']

        # hack because swagger UI doesn't deal with arrays objects well
        params = str(request.data['params'])
        params = ast.literal_eval(params)

        serializer.create_table(repo_name, table_name, params)

        table = serializer.describe_table(repo_name, table_name, False)
        return Response(table, status=status.HTTP_201_CREATED)


class Table(APIView):

    def get(self, request, repo_base, repo_name, table, format=None):
        """
        See the schema of a single table

        This endpoint does not throw an error if the table does not exist.
        """
        username = request.user.get_username()
        serializer = TableSerializer(
            username=username, repo_base=repo_base)

        table_info = serializer.describe_table(repo_name, table, detail=False)
        return Response(table_info, status=status.HTTP_200_OK)

    def delete(self, request, repo_base, repo_name, table, format=None):
        """
        Delete a single table

        Delete will fail is the table in question has a dependencey.
        In this case, you must first delete the dependency.
        """
        username = request.user.get_username()
        serializer = TableSerializer(
            username=username, repo_base=repo_base)
        force = request.data.get('force')

        serializer.delete_table(repo_name, table, force)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class Files(APIView):
    # parser_classes = (FileUploadParser,)

    def get(self, request, repo_base, repo_name, format=None):
        """
        Files in a repo
        """
        username = request.user.get_username()
        serializer = FileSerializer(
            username=username, repo_base=repo_base, request=request)
        files = serializer.list_files(repo_name)
        return Response(files, status=status.HTTP_200_OK)

    def post(self, request, repo_base, repo_name, format=None):
        """
        Create a file

        e.g. $ curl --form file=@FILENAME.CSV
        datahub-local.mit.edu/api/v1/repos/REPO_BASE/REPO_NAME/files
        ---
        omit_serializer: true

        parameters:
          - name: file_format
            in: body
            type: string
            description: format of the file to be created e.g. CSV
          - name: file
            type: file
            paramType: formData,
            description: file to be uploaded
          - name: header
            in: body
            type: string
          - name: delimiter
            in: body
            type: string
          - name: from_table
            in: docstring
            type: string
          - name: from_view
            in: docstring
            type: string
            required: false
          - name: from_card
            in: docstring
            type: string

        """
        username = request.user.get_username()
        file = request.FILES.get('file', None)

        data = request.data
        file_format = data.get('file_format', 'CSV')
        delimiter = data.get('delimiter', ',')
        header = data.get('header', True)

        table = data.get('from_table', None)
        view = data.get('from_view', None)
        card = data.get('from_card', None)

        if file:
            serializer = FileSerializer(username, repo_base, request)
            serializer.upload_file(repo_name, file)
            files = serializer.list_files(repo_name)
            return Response(files, status=status.HTTP_201_CREATED)

        elif table:
            serializer = TableSerializer(username, repo_base, request)
            serializer.export_table(repo_name, table, file_format, delimiter,
                                    header)

            filename = table + "." + file_format
            serializer = FileSerializer(username, repo_base, request)
            file = serializer.get_file(repo_name, filename)
            return Response(file, status=status.HTTP_201_CREATED)

        elif view:
            serializer = ViewSerializer(username, repo_base, request)
            serializer.export_view(repo_name, view, file_format, delimiter,
                                   header)
            filename = view + "." + file_format
            serializer = FileSerializer(username, repo_base, request)
            file = serializer.get_file(repo_name, filename)
            return Response(file, status=status.HTTP_201_CREATED)

        elif card:
            serializer = CardSerializer(username, repo_base, request)
            serializer.export_card(repo_name, card, file_format)

            filename = card + "." + file_format
            serializer = FileSerializer(username, repo_base, request)
            file = serializer.get_file(repo_name, filename)
            return Response(file, status=status.HTTP_201_CREATED)

        else:
            raise(KeyError)

        return Response(
            'specify a {file | [from_table, from_view, from_card ]',
            status=status.HTTP_400_BAD_REQUEST)


class File(APIView):

    def get(self, request, repo_base, repo_name, file_name, format=None):
        """
        See/Download a file
        """
        username = request.user.get_username()
        serializer = FileSerializer(
            username=username, repo_base=repo_base)
        files = serializer.get_file(repo_name, file_name)
        return Response(files, status=status.HTTP_200_OK)

    def delete(self, request, repo_base, repo_name, file_name, format=None):
        """
        Delete a file
        """
        username = request.user.get_username()
        serializer = FileSerializer(
            username=username, repo_base=repo_base)
        serializer.delete_file(repo_name, file_name)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class Views(APIView):

    def get(self, request, repo_base, repo_name, format=None):
        """
        Views in a repo
        """
        username = request.user.get_username()
        serializer = ViewSerializer(
            username=username, repo_base=repo_base, request=request)

        views = serializer.list_views(repo_name)
        return Response(views, status=status.HTTP_200_OK)

    def post(self, request, repo_base, repo_name, format=None):
        """
        Create a view in a repo
        ---
        omit_serializer: true

        parameters:
          - name: view_name
            in: body
            type: string
            description: name of the the view to be created
            required: true
          - name: query
            in: body
            type: string
            description: select query to create the view from
            required: true

        """
        username = request.user.get_username()
        serializer = ViewSerializer(
            username=username, repo_base=repo_base)

        view_name = request.data['view_name']
        query = request.data['query']
        serializer.create_view(repo_name, view_name, query)

        view = serializer.describe_view(repo_name, view_name)
        return Response(view, status=status.HTTP_201_CREATED)


class View(APIView):

    def get(self, request, repo_base, repo_name, view, format=None):
        """
        See the schema of a single view

        This endpoint does not throw an error if the table does not exist.
        """
        username = request.user.get_username()
        serializer = ViewSerializer(
            username=username, repo_base=repo_base)

        view_info = serializer.describe_view(repo_name, view, detail=False)
        return Response(view_info, status=status.HTTP_200_OK)

    def delete(self, request, repo_base, repo_name, view, format=None):
        """
        Delete a single view
        """
        username = request.user.get_username()
        serializer = ViewSerializer(
            username=username, repo_base=repo_base)

        serializer.delete_view(repo_name, view, False)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class Cards(APIView):

    def get(self, request, repo_base, repo_name, format=None):
        """
        Cards in a repo
        """
        username = request.user.get_username()
        serializer = CardSerializer(username, repo_base, request)
        cards = serializer.list_cards(repo_name)
        return Response(cards, status=status.HTTP_200_OK)

    def post(self, request, repo_base, repo_name, format=None):
        """
        Create a card in a repo
        ---
        omit_serializer: true

        parameters:
          - name: card_name
            in: body
            type: string
            description: name of the card to be created
            required: true
          - name: query
            in: body
            description: query to be executed
            type: string
            required: true


        """
        username = request.user.get_username()
        serializer = CardSerializer(username, repo_base, request)
        card_name = request.data['card_name']
        query = request.data['query']
        res = serializer.create_card(repo_name, card_name, query)
        return Response(res, status=status.HTTP_201_CREATED)


class Card(APIView):

    renderer_classes = (api_settings.DEFAULT_RENDERER_CLASSES +
                        [CSVRenderer])
    permission_classes = (api_settings.DEFAULT_PERMISSION_CLASSES +
                          [PublicCardPermission])
    authentication_classes = (api_settings.DEFAULT_AUTHENTICATION_CLASSES +
                              [PublicCardAuthentication])

    def get(self, request, repo_base, repo_name, card_name, format=None):
        """
        See the query and query results of a single card.
        The results of the card query is exactly what the repo base owner
        would see.
        ---
        omit_serializer: true

        parameters:
          - name: current_page
            in: path
            type: integer
            description: page being viewed
          - name: rows_per_page
            in: path
            type: integer
            description: number of rows per page

        produces:
            - application/json
            - text/csv

        """
        username = request.user.get_username()
        data = request.data

        current_page = int(data.get('current_page', 1))
        rows_per_page = int(data.get('rows_per_page', 1000))

        serializer = CardSerializer(username, repo_base, request)
        res = serializer.describe_card(
            repo_name, card_name, current_page, rows_per_page)
        return Response(res, status=status.HTTP_200_OK)

    def patch(self, request, repo_base, repo_name, card_name, format=None):
        """
        Change a card's name, query, and/or make it public or private
        ---
        parameters:
          - name: new_name
            in: path
            type: string
            description: new name for the card
          - name: new_query
            in: path
            type: string
            description: new query for the card
          - name: public
            in: path
            type: bool
            description: whether the card is public or not
        """
        username = request.user.get_username()
        data = request.data
        new_name = data.get('new_name', None)
        new_query = data.get('new_query', None)

        # public needs to be able to parse 'false', so uses json.loads
        public = json.loads(data.get('public', 'null'))

        serializer = CardSerializer(
            username=username, repo_base=repo_base)
        res = serializer.update_card(
            repo_name, card_name, new_query, new_name, public)
        return Response(res, status=status.HTTP_200_OK)

    def delete(self, request, repo_base, repo_name, card_name, format=None):
        """
        Delete a single card
        """
        username = request.user.get_username()
        serializer = CardSerializer(
            username=username, repo_base=repo_base)
        serializer.delete_card(repo_name, card_name)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class Query(APIView):
    """
    manage queries
    """

    renderer_classes = (api_settings.DEFAULT_RENDERER_CLASSES +
                        [CSVRenderer])

    def post(self, request, repo_base, repo_name=None, format=None):
        """
        ---
        omit_serializer: true

        parameters:
          - name: query
            in: body
            type: string
            description: query to be executed
            required: true
          - name: rows_per_page
            in: body
            type: integer
            description: number of rows per page
          - name: current_page
            in: body
            type: integer
            description: page being viewed

        # responseMessages:
        #     - code: 401
        #       message: Not authenticated
        #     - code: 500
        #       message: Internal Service Error
        #     - code: 403
        #       message: You do not have permission to operate on this data
        #     - code: 404
        #       message: Object in question does not exist

        consumes:
            - application/json
        produces:
            - application/json
            - text/csv

        """
        username = request.user.get_username()
        data = request.data
        query = data['query']
        current_page = int(data.get('current_page', 1))
        rows_per_page = int(data.get('rows_per_page', 1000))
        serializer = QuerySerializer(username, repo_base, request)

        result = serializer.execute_query(
            query=query, repo=repo_name, current_page=current_page,
            rows_per_page=rows_per_page,
            rows_only=(request.accepted_media_type == 'text/csv'))
        return Response(result, status=status.HTTP_200_OK)


class RowLevelSecurity(APIView):
    """
    Manage Row Level Security Table based on URl passed params
    """

    def get(self, request, repo_name=None, table=None, format=None):
        """
        List security policies in your repo
        """
        username = request.user.get_username()

        serializer = RowLevelSecuritySerializer(username=username)
        result = serializer.find_security_policies(repo=repo_name, table=table)
        return Response(result, status=status.HTTP_200_OK)

    def post(self, request, repo_name=None, table=None, format=None):
        """
        Create a security policy in a repo. URL parameters overwrite POST body
        ---
        omit_serializer: true

        parameters:
          - name: repo_name
            in: body
            type: string
            description: name of the repo that this applies to
            required: false
          - name: table
            in: body
            description: name of the table that this applies to
            type: string
            required: false
          - name: policy
            in: body
            description: SQL Condition that governs access to the table.
                e.g. "id=1"
            type: string
            required: true
          - name: policy_type
            in: body
            description: SQL privilege being granted. e.g. "select" or "update"
            type: string
            required: true
          - name: grantee
            in: body
            description: the username of the datahub user being granted access
                to these rows
            type: string
            required: true
        """
        username = request.user.get_username()
        serializer = RowLevelSecuritySerializer(username=username)

        if not repo_name:
            repo_name = request.data['repo_name']
        if not table:
            table = request.data['table']

        policy = request.data['policy']
        policy_type = request.data['policy_type']
        grantee = request.data['grantee']

        res = serializer.create_security_policy(
            policy=policy, policy_type=policy_type, grantee=grantee,
            repo=repo_name, table=table)

        if res:
            res = serializer.find_security_policies(
                repo=repo_name,
                table=table,
                policy=policy,
                policy_type=policy_type,
                grantee=grantee)

        return Response(res, status=status.HTTP_201_CREATED)


class RowLevelSecurityById(APIView):
    """
    manage the RLS table based on row IDs
    """
    def patch(self, request, policy_id, format=None):
        """
        Update a security policy of the specified id.
        Ignores additional URL params, and just uses body
        ---
        omit_serializer: true

        parameters:
          - name: policy
            in: body
            description: New SQL Condition that governs access to the table.
                e.g. "accessible = 1"
            type: string
            required: false
          - name: policy_type
            in: body
            description: New SQL privilege being granted. e.g. "select" or
                "update"
            type: string
            required: false
          - name: grantee
            in: body
            description: new datahub user whom this policy applies to
            type: string
            required: false
        """

        username = request.user.get_username()
        serializer = RowLevelSecuritySerializer(username=username)
        policy_id = int(policy_id)
        row = serializer.find_security_policies(policy_id=policy_id)[0]

        # use existing policy values if they aren't specified
        policy = request.data.get('policy', row['policy'])
        policy_type = request.data.get('policy_type', row['policy_type'])
        grantee = request.data.get('grantee', row['grantee'])

        res = serializer.update_security_policy(
            policy_id, policy, policy_type, grantee)

        if res:
            res = serializer.find_security_policies(policy_id=policy_id)

        return Response(res, status=status.HTTP_200_OK)

    def delete(self, request, policy_id, format=None):
        """
        Delete a policy of the specified id
        ---
        """
        username = request.user.get_username()
        serializer = RowLevelSecuritySerializer(username=username)
        policy_id = int(policy_id)

        res = serializer.remove_security_policy(policy_id)

        if res:
            return Response(None, status=status.HTTP_204_NO_CONTENT)


def custom_exception_handler(exc, context):
    result = {}

    # Call REST framework's default exception handler first, to let it handle
    # errors it knows about.
    response = exception_handler(exc, context)
    if response is not None:
        return response

    # Default to a 500 error. If we can't explain what happened, blame
    # ourselves.
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    # Use an appropriate status code for each exception type.
    exceptions_by_status = {
        status.HTTP_400_BAD_REQUEST: [
            ValueError,
            ValidationError,
            PGError,
        ],
        status.HTTP_403_FORBIDDEN: [
            PermissionDenied
        ],
        status.HTTP_404_NOT_FOUND: [
            ObjectDoesNotExist,
            LookupError
        ],
    }
    for drf_status, exceptions in exceptions_by_status.iteritems():
        if next((e for e in exceptions if issubclass(type(exc), e)), None):
            status_code = drf_status
            break

    result['error_type'] = type(exc).__name__
    result['detail'] = exc.message

    # Add extra info for psycopg errors
    if issubclass(type(exc), PGError):
        result['pgcode'] = exc.pgcode
        result['severity'] = exc.diag.severity

    return Response(result, status=status_code)
