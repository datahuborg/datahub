from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^login', 'oidc.authn.provider_login'),
    url(r'^redirect', 'oidc.authn.provider_callback'),
    url(r'^logout', 'oidc.authn.logout'),
)
