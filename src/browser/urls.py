from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

'''
@author: Anant Bhardwaj
@date: Mar 21, 2013

Datahub URL Router
'''

urlpatterns = patterns('',

    ########################################################################################
    ######## ------------------------------ DataHub Core ------------------------- #########
    ########################################################################################

    #### Home Page ####
    url(r'^$', 'browser.views.home'),
    url(r'^about$', 'browser.views.about'),  # for backward compatibility
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),
    #### End Home ####

    #### WWW Pages ####
    url(r'^www/', include('www.urls')),
    #### End WWW Pages ####

    #### Account Related ####
    url(r'^account/', include('account.urls')),
    #### End Account Related ####


    #### Thrift Services ####
    url(r'^service$', 'browser.views.service_core_binary'),
    url(r'^service/account$', 'browser.views.service_account_binary'),
    url(r'^service/json$', 'browser.views.service_core_json'),
    #### End Thrift Services ####


    #### Create ####
    url(r'^create/(\w+)/repo/?$', 'browser.views.repo_create'),

    url(r'^create/(\w+)/(\w+)/card/?$', 'browser.views.card_create'),

    url(r'^create/(\w+)/(\w+)/dashboard/(\w+)/?$', 'browser.views.dashboard_create'),

    url(r'^create/organization/(\w+)/?$', 'browser.views.organization_create'),

    url(r'^create/(\w+)/group/(\w+)/?$', 'browser.views.group_create'),

    url(r'^create/app/(\w+)/?$', 'browser.views.app_create'),

    url(r'^create/annotation/?$', 'browser.views.create_annotation'),
    #### End Create ####


    #### Browse ####
    url(r'^browse/(\w+)/(\w+)/table/(\w+)/?$', 'browser.views.table'),

    url(r'^browse/(\w+)/(\w+)/query/?$', 'browser.views.query'),

    url(r'^browse/(\w+)/(\w+)/card/(.+)/?$', 'browser.views.card'),

    url(r'^browse/(\w+)/(\w+)/dashboard/(\w+)/?$', 'browser.views.dashboard'),

    url(r'^browse/(\w+)/(\w+)/?$', 'browser.views.repo'),

    url(r'^browse/(\w+)/(\w+)/tables/?$', 'browser.views.repo_tables'),

    url(r'^browse/(\w+)/(\w+)/files/?$', 'browser.views.repo_files'),

    url(r'^browse/(\w+)/(\w+)/cards/?$', 'browser.views.repo_cards'),

    url(r'^browse/(\w+)/(\w+)/dashboards/?$', 'browser.views.repo_dashboards'),

    url(r'^browse/(\w+)/?$', 'browser.views.user'),
    #### End Browse ####


    ### Delete ####
    url(r'^delete/(\w+)/(\w+)/?$', 'browser.views.repo_delete'),

    url(r'^delete/(\w+)/(\w+)/table/(\w+)/?$', 'browser.views.table_delete'),

    url(r'^delete/(\w+)/(\w+)/card/(\w+)/?$', 'browser.views.card_delete'),

    url(r'^delete/(\w+)/(\w+)/dashboard/(\w+)/?$', 'browser.views.dashboard_delete'),

    url(r'^delete/(\w+)/(\w+)/file/([\w\d\-\.]+)/?$', 'browser.views.file_delete'),
    ### End Delete ####


    ### Export ###
    url(r'^export/(\w+)/(\w+)/table/(\w+)/?$', 'browser.views.table_export'),

    url(r'^export/(\w+)/(\w+)/query/?$', 'browser.views.query_export'),

    url(r'^export/(\w+)/(\w+)/card/(\w+)/?$', 'browser.views.card_export'),
    ### End Export ####


    ### Special File Operations ####
    url(r'^upload/(\w+)/(\w+)/file/?$', 'browser.views.file_upload'),
    url(r'^import/(\w+)/(\w+)/file/([\w\d\-\.]+)', 'browser.views.file_import'),
    url(r'^download/(\w+)/(\w+)/file/([\w\d\-\.]+)', 'browser.views.file_download'),
    ### End Special File Operations ####


    #### Settings ####
    url(r'^settings/(\w+)/(\w+)/?$', 'browser.views.repo_settings'),

    url(r'^settings/(\w+)/?$', 'browser.views.user_settings'),
    #### End Settings ####


    ### Collaborators ###
    url(r'^collaborator/repo/(\w+)/(\w+)/add/?$', 'browser.views.repo_collaborators_add'),

    url(r'^collaborator/repo/(\w+)/(\w+)/remove/(\w+)/?$', 'browser.views.repo_collaborators_remove'),
    ### End Collaborators ###

    ### Developer Apps ###
    url(r'^developer/apps/?$', 'browser.views.apps'),

    url(r'^developer/apps/register/?$', 'browser.views.apps_register'),

    url(r'^developer/apps/remove/(\w+)/?$', 'browser.views.app_remove'),
    ### End Apps ###

    ### Permissions ###
    url(r'^permissions/apps/allow_access/(\w+)/(\w+)$', 'browser.views.app_allow_access'),

    url(r'^api/rest/', include('api.rest.urls')), # REST APIs

    ########################################################################################
    ######## ------------------------------ END DataHub Core --------------------- #########
    ########################################################################################


    #### Apps ####
    url(r'^apps/console/', include('console.urls')), # console app
    url(r'^apps/refiner/', include('refiner.urls')), # refiner app
    url(r'^apps/dbwipes/', include('dbwipes.urls')), # dbwipes app
    url(r'^apps/viz/', include('viz2.urls')), # viz app
    url(r'^apps/sentiment/', include('sentiment.urls')), # sentiment app
    url(r'^apps/dataq/', include('dataq.urls')), # dataq app
    url(r'^apps/datatables/', include('datatables.urls')), # datatables app
    #### End Apps ####
)
