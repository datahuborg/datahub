from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^login', 'browser.auth.login'),
    url(r'^register', 'browser.auth.register'),
    url(r'^logout', 'browser.auth.logout'),

    url(r'^forgot', 'browser.auth.forgot'),
    url(r'^reset/(\w+)', 'browser.auth.reset'),
    url(r'^settings', 'browser.auth.settings'),
    url(r'^verify/(\w+)', 'browser.auth.verify'),

    url(r'^$', 'browser.views.home'),

    url(r'^console$', 'browser.views.console'),
    url(r'^console/$', 'browser.views.console'),

    url(r'^visualize$', 'browser.views.visualize'),
    url(r'^visualize/$', 'browser.views.visualize'),

    url(r'^newrepo$', 'browser.views.newrepo'),
    url(r'^newrepo/$', 'browser.views.newrepo'),

    url(r'^create_table_from_file$', 'browser.views.create_table_from_file'),

    url(r'^service$', 'browser.views.service_binary'),
    url(r'^service/binary$', 'browser.views.service_binary'),
    url(r'^service/json$', 'browser.views.service_json'),

    url(r'^browse/(\w+)/(\w+)/(\w+)$', 'browser.views.table'),
    url(r'^browse/(\w+)/(\w+)/(\w+)/(\w+)$', 'browser.views.table'),
    url(r'^browse/(\w+)/(\w+)/(\w+)/(\w+)/$', 'browser.views.table'),

    url(r'^browse/(\w+)/(\w+)$', 'browser.views.repo'),
    url(r'^browse/(\w+)/(\w+)/$', 'browser.views.repo'),

    url(r'^browse/(\w+)$', 'browser.views.user'),
    url(r'^browse/(\w+)/$', 'browser.views.user')
)