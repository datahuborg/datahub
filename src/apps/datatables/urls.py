from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^api/table/(?P<repo>\w+)/(?P<table>\w+)/$', 'datatables.views.table'),
    url(r'^api/schema/(?P<repo>\w+)/(?P<table>\w+)/$', 'datatables.views.schema')
)
