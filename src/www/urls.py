from django.conf.urls import patterns, include, url

urlpatterns = patterns('',    
    url(r'^$', 'www.views.index'),
    url(r'^developer$', 'www.views.developer_apis'),
    url(r'^developer/$', 'www.views.developer_apis'),
)