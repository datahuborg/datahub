from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [

    # v1 api
    url(r'^v1/user/$', views.user, name='user'),
    url(r'^v1/user/repos/$', views.user_repos, name='user_repos'),
    url(r'^v1/repos/$', views.user_accessible_repos,
        name='user_accessible_repos'),

    url(r'^v1/repos/(\w+)/?', views.collaborator_repos,
        name='collaborator_repos'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
