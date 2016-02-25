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
    url(r'^v1/repos/(\w+)/?$', views.ReposForUser.as_view(),
        name='repos_specific'),
    url(r'^v1/repos/(\w+)/(\w+)/?$', views.Repo.as_view(),
        name='repo'),




    # collaborators
    url(r'^v1/repos/(\w+)/(\w+)/collaborators/(\w+)/?$',
        views.Collaborator.as_view(), name='collaborator'),
    url(r'^v1/repos/(\w+)/(\w+)/collaborators/?$',
        views.Collaborators.as_view(), name='collaborators'),

    # tables
    url(r'^v1/repos/(\w+)/(\w+)/tables/(\w+)/?$',
        views.Table.as_view(), name='table'),
    url(r'^v1/repos/(\w+)/(\w+)/tables/?$',
        views.Tables.as_view(), name='tables'),

    # views
    url(r'^v1/repos/(\w+)/(\w+)/views/(\w+)/?$',
        views.View.as_view(), name='view'),
    url(r'^v1/repos/(\w+)/(\w+)/views/?$',
        views.Views.as_view(), name='views'),

    # cards
    url(r'^v1/repos/(\w+)/(\w+)/cards/(\w+)/?$',
        views.Card.as_view(), name='card'),
    url(r'^v1/repos/(\w+)/(\w+)/cards/?$',
        views.Cards.as_view(), name='cards'),

    # files
    url(r'^v1/repos/(\w+)/(\w+)/files/([\w\s\.]+)$',
        views.File.as_view(), name='file'),
    url(r'^v1/repos/(\w+)/(\w+)/files/?$',
        views.Files.as_view(), name='files'),

    # query
    url(r'^v1/query/(\w+)/(\w+)/?$', views.Query.as_view(),
        name='query_with_repo'),
    url(r'^v1/query/(\w+)/?$', views.Query.as_view(),
        name='query'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
