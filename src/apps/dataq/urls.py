from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^api/$', 'dataq.views.repos'),
    url(r'^api/(?P<repo_name>\w+)/$', 'dataq.views.tables'),
    url(r'api/(?P<repo_name>\w+)/(?P<table_name>\w+)/$', 'dataq.views.schema'),
)
