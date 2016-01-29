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

        self.manager = DataHubManager(
            user=self.username, repo_base=self.repo_base)

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


class RepoSerializer(DataHubSerializer):
    def __init__(self, *args, **kwargs):

        self.include_own = kwargs.get('include_own')
        self.include_all_collabs = kwargs.get('include_all_collabs')
        self.include_specific_collab = kwargs.get('include_specific_collab')

        kwargs.pop('include_own', None)
        kwargs.pop('include_all_collabs', None)
        kwargs.pop('include_specific_collab', None)

        super(RepoSerializer, self).__init__(*args, **kwargs)

    @property
    def _own_repos(self):
        manager = DataHubManager(user=self.username, repo_base=self.username)
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

        return repo_obj_list

    @property
    def _specific_collab_repos(self):
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

        return repo_obj_list

    @property
    def _all_collab_repos(self):
        manager = DataHubManager(user=self.username, repo_base=self.username)
        collab_repos = manager.list_collaborator_repos()

        repo_obj_list = []
        for repo in collab_repos:
            collaborators = manager.list_collaborators(repo.repo_name)

            repo_obj_list.append({
                'repo_name': repo.repo_name,
                'permission': repo.permission,
                'owner': repo.repo_base,
                'collaborators': collaborators
                })

        return repo_obj_list

    def create(self, validated_data):
        import pdb; pdb.set_trace()
        self.manager.create_repo(validated_data)
        # create a repo for the user

    def to_representation(self, obj):
        combined_repos = []

        if self.include_own:
            combined_repos += self._own_repos

        if self.include_all_collabs:
            combined_repos += self._all_collab_repos
        elif self.include_specific_collab:
            combined_repos += self._specific_collab_repos
        return {'repos': combined_repos}
