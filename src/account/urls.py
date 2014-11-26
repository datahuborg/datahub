from django.conf.urls import patterns, include, url

urlpatterns = patterns('',    
    url(r'^login', 'account.auth.login'),
    url(r'^register', 'account.auth.register'),
    url(r'^logout', 'account.auth.logout'),

    url(r'^forgot', 'account.auth.forgot'),
    url(r'^jdbc_password', 'account.auth.jdbc_password'),
    url(r'^reset/(\w+)', 'account.auth.reset'),
    url(r'^verify/(\w+)', 'account.auth.verify'),
)