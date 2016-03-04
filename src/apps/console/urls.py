from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'console.views.index'),
    url(r'^console2/?$', 'console.views.index2'))
