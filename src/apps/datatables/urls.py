from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^api/table/(?P<repo>\w+)/(?P<table>\w+)/$', 'datatables.views.table'),
    url(r'^api/schema/(?P<repo>\w+)/(?P<table>\w+)/$', 'datatables.views.schema'),
    url(r'^api/aggregate/(?P<repo>\w+)/(?P<table>\w+)/(?P<agg_type>\w+)/(?P<col_name>\w+)/$', 'datatables.views.aggregate')
)
