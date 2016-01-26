from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view

from inventory.models import Collaborator
from .serializer import UserSerializer, UserRepoSerializer, CollaboratorRepoSerializer


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

    serializer = UserRepoSerializer(username=username, repo_base=repo_base)
    return Response(serializer.data)

@api_view(['GET'])
@login_required
def all_repos(request, format=None):
    
    username = request.user.get_username()
    repo_base = username
    own_serializer = UserRepoSerializer(username=username, repo_base=repo_base)

    user = User.objects.get(username=username)
    collaborators = Collaborator.objects.filter(user=user)
    collab_serializer = CollaboratorRepoSerializer(collaborators, many=True)


    return Response(own_serializer.data + collab_serializer.data)

    # get own repos
    # and all repos


@api_view(['GET'])
@login_required
def collaborator_repos(request, repo_base, format=None):
    username = request.user.get_username()

    if username == repo_base:
        return own_repos(request)

    user = User.objects.get(username=username)
    collaborators = Collaborator.objects.filter(user=user)
    serializer = CollaboratorRepoSerializer(collaborators, many=True)
    return Response(serializer.data)
