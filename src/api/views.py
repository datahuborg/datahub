from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializer import UserSerializer, UserRepoSerializer


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

    serializer = UserRepoSerializer(username=username, repo_base=repo_base)
    return Response(serializer.data)

