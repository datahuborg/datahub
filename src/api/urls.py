from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [

    # v1 api
    url(r'^v1/user/$', views.user, name='user'),
    url(r'^v1/user/repos/$', views.own_repos, name='user_repos'),
    url(r'^v1/repos/$', views.all_repos, name='repos_convenience'),

    url(r'^v1/repos/$', views.own_repos, name='own_repos'),
    url(r'^v1/repos/(\w+)/?', views.collaborator_repos, name='collaborator_repos'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
