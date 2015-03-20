from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^(?P<table>\w+)/$', 'datatables.views.table')
)
