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
    url(r'^api$', 'browser.views.api'),
    url(r'^(\w+)/(\w+)/(\w+)$', 'browser.views.table'),
    url(r'^(\w+)/(\w+)', 'browser.views.repo'),
    url(r'^(\w+)', 'browser.views.user')
)