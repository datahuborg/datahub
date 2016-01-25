from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^v1/user/$', views.user),
    url(r'^v1/user/(?P<pk>[0-9]+)$', views.user),
]

urlpatterns = format_suffix_patterns(urlpatterns)
