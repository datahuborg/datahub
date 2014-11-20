from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
	url(r'^page/(\w+)/(\w+)/(\w+)$', 'dbwipes.views.index'),
    url(r'^page/(\w+)/(\w+)/(\w+)/$', 'dbwipes.views.index'),

    url(r'^api/databases$', 'dbwipes.views.dbs'),
    url(r'^api/databases/$', 'dbwipes.views.dbs'),
    url(r'^api/tables$', 'dbwipes.views.tables'),
    url(r'^api/tables/$', 'dbwipes.views.tables'),
    url(r'^api/schema$', 'dbwipes.views.schema'),
    url(r'^api/schema/$', 'dbwipes.views.schema'),
    url(r'^api/tuples/$', 'dbwipes.views.api_tuples'),
    url(r'^api/query/$', 'dbwipes.views.api_query'),
    url(r'^api/column_distribution/$', 'dbwipes.views.column_distribution'),
    url(r'^api/column_distributions/$', 'dbwipes.views.column_distributions'),
    url(r'^api/requestid/$', 'dbwipes.views.requestid'),
    url(r'^api/status/$', 'dbwipes.views.api_status'),
    url(r'^api/scorpion$', 'dbwipes.views.scorpion'),
    url(r'^api/scorpion/$', 'dbwipes.views.scorpion'),
)