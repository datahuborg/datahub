import json

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializer import (
    UserSerializer, RepoSerializer, CollaboratorSerializer, TableSerializer)


@api_view(['GET'])
@login_required
def user(request, format=None):
    username = request.user.get_username()
    user = User.objects.get(username=username)

    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@login_required
def user_repos(request, format=None):
    username = request.user.get_username()
    repo_base = username

    serializer = RepoSerializer(username=username, repo_base=repo_base)
    return Response(serializer.user_owned_repos)


@api_view(['GET'])
@login_required
def user_accessible_repos(request, format=None):
    username = request.user.get_username()
    repo_base = username
    serializer = RepoSerializer(username=username, repo_base=repo_base)

    return Response(serializer.user_accessible_repos())


@api_view(['GET', 'POST'])
@login_required
def collaborator_repos(request, repo_base, format=None):
    username = request.user.get_username()
    serializer = RepoSerializer(username=username, repo_base=repo_base)

    if request.method == 'GET':
        if username == repo_base:
            return Response(serializer.user_owned_repos())
        else:
            return Response(serializer.specific_collab_repos(repo_base))

    elif request.method == 'POST':
        # body = json.loads(request.body)
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


@api_view(['DELETE', 'PATCH'])
@login_required
def delete_rename_repo(request, repo_base, repo_name):
    username = request.user.get_username()
    serializer = RepoSerializer(username=username, repo_base=repo_base)

    if request.method == 'DELETE':
        success = serializer.delete_repo(repo_name=repo_name, force=True)
        if success:
            return Response(
                serializer.user_accessible_repos(),
                status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.user_accessible_repos(),
                status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
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


@api_view(['GET'])
@login_required
def list_collaborators(request, repo_base, repo):
    username = request.user.get_username()
    serializer = CollaboratorSerializer(username=username, repo_base=repo_base)
    collaborators = serializer.list_collaborators(repo)

    return Response(collaborators, status=status.HTTP_200_OK)


@api_view(['PUT', 'DELETE'])
@login_required
def add_or_remove_collaborator(request, repo_base, repo, collaborator):
    username = request.user.get_username()
    serializer = CollaboratorSerializer(username=username, repo_base=repo_base)
    if request.method == 'PUT':
        # it's unclear why we have to use request.body here, instead
        # of using request.data (from rest_framework.request) or request.POST
        # it seems like rest_framework isn't correctly parsing json.
        # {"privileges": ["UPDATE"]}
        privileges = json.loads(request.body)['privileges']
        success = serializer.add_collaborator(repo, collaborator, privileges)
        collaborators = serializer.list_collaborators(repo)
        if success:
            return Response(collaborators, status=status.HTTP_200_OK)
        else:
            return Response(collaborators, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        success = serializer.remove_collaborator(repo, collaborator)
        collaborators = serializer.list_collaborators(repo)
        if success:
            return Response(collaborators, status=status.HTTP_200_OK)
        else:
            return Response(collaborators, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@login_required
def create_or_list_tables(request, repo_base, repo):
    username = request.user.get_username()
    serializer = TableSerializer(
        username=username, repo_base=repo_base)

    if request.method == 'GET':
        # list all tables
        tables = serializer.list_tables(repo)
        return Response(tables, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        params = request.data['params']
        table_name = request.data['table_name']
        success = serializer.create_table(repo, table_name, params)

        tables = serializer.list_tables(repo)
        if success:
            return Response(tables, status=status.HTTP_200_OK)
        else:
            return Response(tables, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@login_required
def view_table_info(request, repo_base, repo, table):
    username = request.user.get_username()
    serializer = TableSerializer(
        username=username, repo_base=repo_base)

    table_info = serializer.describe_table(repo, table, detail=False)
    if table_info:
        return Response(table_info, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
