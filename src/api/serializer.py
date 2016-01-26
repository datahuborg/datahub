from rest_framework import serializers
from django.contrib.auth.models import User

from inventory.models import Collaborator
from core.db.manager import DataHubManager


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'last_login', 'first_name', 'last_name', 'email')


class DataHubSerializer(serializers.BaseSerializer):

    def __init__(self, *args, **kwargs):
        self.username = kwargs['username']
        self.repo_base = kwargs['repo_base']

        kwargs.pop('username')
        kwargs.pop('repo_base')

        super(DataHubSerializer, self).__init__(*args, **kwargs)

        # fill in self.instance, because the BaseSerializer class is
        # tighly coupled with django models. By just adding in a variable,
        # checks for None pass
        self.instance = 'dummy_instance'

    def is_valid(self, raise_exception=False):
        super(DataHubManager, self).is_valid(raise_exception=False)

    def to_representation(self, obj):
        message = ('DataHubSerializer is meant to be abstract')
        raise NotImplementedError(message)


class UserRepoSerializer(DataHubSerializer):
    def __init__(self, *args, **kwargs):
        super(UserRepoSerializer, self).__init__(*args, **kwargs)

    def to_representation(self, obj):
        manager = DataHubManager(user=self.username, repo_base=self.repo_base)
        repos = manager.list_repos()
        repos.sort()
        return repos


class CollaboratorRepoSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(CollaboratorRepoSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Collaborator
        fields = ('repo_name', 'permission', 'user')
