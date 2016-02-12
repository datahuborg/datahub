from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [

    # user
    url(r'^v1/user/$', views.user, name='user'),
    url(r'^v1/user/repos/$', views.user_repos, name='user_repos'),
    url(r'^v1/repos/$', views.user_accessible_repos,
        name='user_accessible_repos'),

    # collaborators
    url(r'^v1/repos/(\w+)/(\w+)/collaborators/(\w+)/?',
        views.add_or_remove_collaborator, name='add_or_remove_collaborator'),
    url(r'^v1/repos/(\w+)/(\w+)/collaborators/?', views.list_collaborators,
        name='list_collaborators'),

    # tables
    url(r'^v1/repos/(\w+)/(\w+)/tables/?',
        views.create_or_list_tables, name='create_or_list_tables'),

    # repos
    url(r'^v1/repos/(\w+)/(\w+)/?', views.delete_rename_repo,
        name='delete_rename_repo'),
    url(r'^v1/repos/(\w+)/?', views.collaborator_repos,
        name='collaborator_repos'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
