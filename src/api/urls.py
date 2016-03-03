from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [

    # user
    url(r'^v1/user/?$', views.CurrentUser.as_view(), name='user'),
    url(r'^v1/user/repos/?$', views.CurrentUserRepos.as_view(),
        name='user_repos'),

    # repos
    url(r'^v1/repos/?$', views.Repos.as_view(),
        name='repos_all'),
    url(r'^v1/repos/(?P<repo_base>\w+)/?$', views.ReposForUser.as_view(),
        name='repos_specific'),
    url(r'^v1/repos/(?P<repo_base>\w+)/(?P<repo_name>\w+)/?$', views.Repo.as_view(),
        name='repo'),

    # collaborators
    url(r'^v1/repos/(?P<repo_base>\w+)/(?P<repo_name>\w+)/collaborators/(?P<collaborator>\w+)/?$',
        views.Collaborator.as_view(), name='collaborator'),
    url(r'^v1/repos/(?P<repo_base>\w+)/(?P<repo_name>\w+)/collaborators/?$',
        views.Collaborators.as_view(), name='collaborators'),

    # tables
    url(r'^v1/repos/(?P<repo_base>\w+)/(?P<repo_name>\w+)/tables/(?P<table>\w+)/?$',
        views.Table.as_view(), name='table'),
    url(r'^v1/repos/(?P<repo_base>\w+)/(?P<repo_name>\w+)/tables/?$',
        views.Tables.as_view(), name='tables'),

    # views
    url(r'^v1/repos/(?P<repo_base>\w+)/(?P<repo_name>\w+)/views/(?P<view>\w+)/?$',
        views.View.as_view(), name='view'),
    url(r'^v1/repos/(?P<repo_base>\w+)/(?P<repo_name>\w+)/views/?$',
        views.Views.as_view(), name='views'),

    # cards
    url(r'^v1/repos/(?P<repo_base>\w+)/(?P<repo_name>\w+)/cards/(?P<card_name>\w+)/?$',
        views.Card.as_view(), name='card'),
    url(r'^v1/repos/(?P<repo_base>\w+)/(?P<repo_name>\w+)cards/?$',
        views.Cards.as_view(), name='cards'),

    # files
    url(r'^v1/repos/(?P<repo_base>\w+)/(?P<repo_name>\w+)/files/(?P<file_name>[\w\s\.]+)$',
        views.File.as_view(), name='file'),
    url(r'^v1/repos/(?P<repo_base>\w+)/(?P<repo_name>\w+)/files/?$',
        views.Files.as_view(), name='files'),

    # query
    url(r'^v1/query/(?P<repo_base>\w+)/(?P<repo_name>\w+)/?$',
        views.Query.as_view(), name='query_with_repo'),
    url(r'^v1/query/(?P<repo_base>\w+)/?$', views.Query.as_view(),
        name='query'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
