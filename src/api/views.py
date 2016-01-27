from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializer import (UserSerializer, RepoSerializer)


@api_view(['GET'])
@login_required
def user(request, format=None):
    username = request.user.get_username()
    user = User.objects.get(username=username)

    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@login_required
def own_repos(request, format=None):
    username = request.user.get_username()
    repo_base = username

    serializer = RepoSerializer(username=username, repo_base=repo_base,
                                include_own=True)
    return Response(serializer.data)


# WORKS!
@api_view(['GET'])
@login_required
def all_repos(request, format=None):
    username = request.user.get_username()
    repo_base = username
    serializer = RepoSerializer(username=username, repo_base=repo_base,
                                include_own=True,
                                include_all_collabs=True)

    return Response(serializer.data)


@api_view(['GET', 'POST'])
@login_required
def collaborator_repos(request, repo_base, format=None):
    # GET
    username = request.user.get_username()

    include_specific_collab, include_own = True, False
    # if the user is actually just requesting their own repos
    if username == repo_base:
        include_specific_collab, include_own = False, True

    serializer = RepoSerializer(username=username, repo_base=repo_base,
                                include_own=include_own,
                                include_all_collabs=include_specific_collab)


    return Response(serializer.data)

    # # POST
    # if request.method == 'POST':
    #     repo = request.POST['repo']
    #     manager = DataHubManager(user=username, repo_base=repo_base)
    #     manager.create_repo(repo)