from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'viz2.views.index'),
)
