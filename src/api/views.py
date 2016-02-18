from django.contrib.auth.models import User

from psycopg2 import Error

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.views import exception_handler
from rest_framework.response import Response


from .serializer import (
    UserSerializer, RepoSerializer, CollaboratorSerializer,
    TableSerializer, QuerySerializer)


class CurrentUser(APIView):
    """The current user."""

    def get(self, request, format=None):
        username = request.user.get_username()
        user = User.objects.get(username=username)

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)


class CurrentUserRepos(APIView):
    """The repos owned by the current user."""

    def get(self, request, format=None):
        username = request.user.get_username()
        repo_base = username

        serializer = RepoSerializer(username=username, repo_base=repo_base)
        return Response(serializer.user_owned_repos())


class Repos(APIView):
    """The repos visible to the current user."""

    def get(self, request, format=None):
        username = request.user.get_username()
        repo_base = username

        serializer = RepoSerializer(username=username, repo_base=repo_base)
        return Response(serializer.user_accessible_repos())


class ReposForUser(APIView):
    """
    The repos of a specific user.

    POST to create a repo under the specified user. Fails if the specified
    user isn't the current user.
    """

    def get(self, request, repo_base, format=None):
        username = request.user.get_username()
        serializer = RepoSerializer(username=username, repo_base=repo_base)

        if username == repo_base:
            return Response(serializer.user_owned_repos())
        else:
            return Response(serializer.specific_collab_repos(repo_base))

    def post(self, request, repo_base, format=None):
        username = request.user.get_username()
        serializer = RepoSerializer(username=username, repo_base=repo_base)

        repo_name = request.data['repo']
        success = serializer.create_repo(repo_name)
        if success:
            return Response(
                serializer.user_accessible_repos(),
                status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.user_accessible_repos(),
                status=status.HTTP_400_BAD_REQUEST)


class Repo(APIView):
    """
    A specific repo of a specific user.

    DELETE to delete the repo.
    PATCH to rename the repo.
    """

    def delete(self, request, repo_base, repo_name, format=None):
        username = request.user.get_username()
        serializer = RepoSerializer(username=username, repo_base=repo_base)
        success = serializer.delete_repo(repo_name=repo_name, force=True)

        if success:
            return Response(
                serializer.user_accessible_repos(),
                status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.user_accessible_repos(),
                status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, repo_base, repo_name, format=None):
        username = request.user.get_username()
        serializer = RepoSerializer(username=username, repo_base=repo_base)
        new_repo_name = request.data['new_name']
        success = serializer.rename_repo(
            repo=repo_name, new_name=new_repo_name)

        if success:
            return Response(
                serializer.user_accessible_repos(),
                status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.user_accessible_repos(),
                status=status.HTTP_400_BAD_REQUEST)


class Collaborators(APIView):
    """
    List and create collaborators.

    GET to list the collaborators.
    POST to add a collaborator.
    """

    def get(self, request, repo_base, repo, format=None):
        username = request.user.get_username()
        serializer = CollaboratorSerializer(username=username,
                                            repo_base=repo_base)
        collaborators = serializer.list_collaborators(repo)

        return Response(collaborators, status=status.HTTP_200_OK)

    def post(self, request, repo_base, repo, format=None):
        username = request.user.get_username()
        serializer = CollaboratorSerializer(username=username,
                                            repo_base=repo_base)
        data = request.data
        collaborator = data['user']
        privileges = data['privileges']
        success = serializer.add_collaborator(repo, collaborator, privileges)
        collaborators = serializer.list_collaborators(repo)
        if success:
            return Response(collaborators, status=status.HTTP_200_OK)
        else:
            return Response(collaborators, status=status.HTTP_400_BAD_REQUEST)


class Collaborator(APIView):
    """
    Modify and delete existing collaborators.

    DELETE to remove the specified collaborator from the repo.
    PUT to modify the privileges of an existing collaborator.
    """

    def delete(self, request, repo_base, repo, collaborator, format=None):
        username = request.user.get_username()
        serializer = CollaboratorSerializer(username=username,
                                            repo_base=repo_base)
        success = serializer.remove_collaborator(repo, collaborator)
        collaborators = serializer.list_collaborators(repo)
        if success:
            return Response(collaborators, status=status.HTTP_200_OK)
        else:
            return Response(collaborators, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, repo_base, repo, collaborator, format=None):
        username = request.user.get_username()
        serializer = CollaboratorSerializer(username=username,
                                            repo_base=repo_base)
        data = request.data
        privileges = data['privileges']
        success = serializer.add_collaborator(repo, collaborator, privileges)
        collaborators = serializer.list_collaborators(repo)
        if success:
            return Response(collaborators, status=status.HTTP_200_OK)
        else:
            return Response(collaborators, status=status.HTTP_400_BAD_REQUEST)


class Tables(APIView):
    """
    List and create tables.

    GET to list existing tables.
    POST to create a new table.
    """

    def get(self, request, repo_base, repo, format=None):
        username = request.user.get_username()
        serializer = TableSerializer(
            username=username, repo_base=repo_base)

        tables = serializer.list_tables(repo)
        return Response(tables, status=status.HTTP_200_OK)

    def post(self, request, repo_base, repo, format=None):
        username = request.user.get_username()
        serializer = TableSerializer(
            username=username, repo_base=repo_base)

        params = request.data['params']
        table_name = request.data['table_name']
        success = serializer.create_table(repo, table_name, params)

        tables = serializer.list_tables(repo)
        if success:
            return Response(tables, status=status.HTTP_200_OK)
        else:
            return Response(tables, status=status.HTTP_400_BAD_REQUEST)


class Table(APIView):
    """
    View a single table.

    GET to view info about a table.
    """

    def get(self, request, repo_base, repo, table):
        username = request.user.get_username()
        serializer = TableSerializer(
            username=username, repo_base=repo_base)

        table_info = serializer.describe_table(repo, table, detail=False)
        if table_info:
            return Response(table_info, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Query(APIView):
    """
    Manage SQL queries.

    POST execute a SQL statement and receive the result.
    """

    def post(self, request, repo_base, repo=None, format=None):
        username = request.user.get_username()
        data = request.data
        query = data['sql']
        serializer = QuerySerializer(username=username, repo_base=repo_base)

        result = serializer.execute_sql(query=query, repo=repo)
        return Response(result, status=status.HTTP_200_OK)


def custom_exception_handler(exc, context):
    result = {}

    # Now add the HTTP status code to the response.
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code
    elif issubclass(type(exc), Error):
        result['error_type'] = type(exc).__name__
        result['message'] = exc.message
        result['pgcode'] = exc.pgcode
        result['severity'] = exc.diag.severity
    else:
        result = exc

    return Response(result, status=status.HTTP_400_BAD_REQUEST)
