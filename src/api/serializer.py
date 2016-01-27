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

        # fill in self.instance, because the BaseSerializer class is
        # tighly coupled with django models. By just adding in a variable,
        # checks for None pass
        if args == ():
            args = ('dummy_instance',)

        super(DataHubSerializer, self).__init__(*args, **kwargs)

    def is_valid(self, raise_exception=False):
        super(DataHubManager, self).is_valid(raise_exception=False)

    def to_representation(self, obj):
        message = ('DataHubSerializer is meant to be abstract. '
                   'You must implement the to_representation() method.')
        raise NotImplementedError(message)


class UserRepoSerializer(DataHubSerializer):
    def __init__(self, *args, **kwargs):
        super(UserRepoSerializer, self).__init__(*args, **kwargs)

    def to_representation(self, obj):
        manager = DataHubManager(user=self.username, repo_base=self.repo_base)
        repos = manager.list_repos()
        repos.sort()

        repo_obj_list = []
        for repo in repos:
            collaborators = manager.list_collaborators(repo)

            repo_obj_list.append({
                'repo_name': repo,
                'permissions': 'ALL',
                'collaborators': collaborators,
                'owner': self.username
                })

        repos = {'repos': repo_obj_list}
        return repos


class CollaboratorRepoSerializer(DataHubSerializer):
    def __init__(self, *args, **kwargs):
        super(CollaboratorRepoSerializer, self).__init__(*args, **kwargs)

    def to_representation(self, obj):
        manager = DataHubManager(user=self.username, repo_base=self.repo_base)

        # get the collaborators
        user = User.objects.get(username=self.username)
        collab_repos = Collaborator.objects.filter(user=user)

        repo_obj_list = []
        for repo in collab_repos:
            collaborators = manager.list_collaborators(repo.repo_name)

            repo_obj_list.append({
                'repo_name': repo.repo_name,
                'permission': repo.permission,
                'owner': repo.repo_base,
                'collaborators': collaborators
                })

        return {'repos': repo_obj_list}
