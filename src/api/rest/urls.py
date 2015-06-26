from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^connection/open', 'api.rest.handler.connection_open'),
    url(r'^connection/close', 'api.rest.handler.connection_close'),
    url(r'^connection/repo_create$', 'api.rest.handler.repo_create'),
    url(r'^connection/repo_delete$', 'api.rest.handler.repo_delete'),
    url(r'^connection/repo_list$', 'api.rest.handler.repo_list'),
    url(r'^connection/execute_query$', 'api.rest.handler.execute_query'),
)