from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'www.views.index', name='index')
)
