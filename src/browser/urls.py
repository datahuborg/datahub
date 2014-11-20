from django.conf.urls import patterns, include, url

urlpatterns = patterns('', 
    #### WWW pages ####
    url(r'^$', 'browser.views.home'),
    url(r'^about$', 'browser.views.about'),
    url(r'^developer$', 'browser.views.developer_apis'),
    url(r'^developer/$', 'browser.views.developer_apis'),
    #### End WWW pages ####

    #### Account Related ####
    url(r'^login', 'browser.auth.login'),
    url(r'^register', 'browser.auth.register'),
    url(r'^logout', 'browser.auth.logout'),

    url(r'^forgot', 'browser.auth.forgot'),
    url(r'^reset/(\w+)', 'browser.auth.reset'),
    url(r'^verify/(\w+)', 'browser.auth.verify'),
    #### End Account Related ####


    #### Thrift Services ####
    url(r'^service$', 'browser.views.service_binary'),
    url(r'^service/binary$', 'browser.views.service_binary'),
    url(r'^service/json$', 'browser.views.service_json'),
    #### End Thrift Services ####


    #### Create ####
    url(r'^create/repo/(\w+)$', 'browser.views.repo_create'),
    url(r'^create/repo/(\w+)/$', 'browser.views.repo_create'),

    url(r'^create/organization/(\w+)$', 'browser.views.organization_create'),
    url(r'^create/organization/(\w+)/$', 'browser.views.organization_create'),

    url(r'^create/group/(\w+)/(\w+)$', 'browser.views.group_create'),
    url(r'^create/group/(\w+)/(\w+)/$', 'browser.views.group_create'),

    url(r'^create/app/(\w+)$', 'browser.views.app_create'),
    url(r'^create/app/(\w+)/$', 'browser.views.app_create'),

    url(r'^create/card/(\w+)/(\w+)/(\w+)$', 'browser.views.card_create'),
    url(r'^create/card/(\w+)/(\w+)/(\w+)/$', 'browser.views.card_create'),

    url(r'^create/dashboard/(\w+)/(\w+)/(\w+)$', 'browser.views.dashboard_create'),
    url(r'^create/dashboard/(\w+)/(\w+)/(\w+)/$', 'browser.views.dashboard_create'),
    #### End Create ####
 

    #### Browse ####
    url(r'^browse/(\w+)/(\w+)/table/(\w+)$', 'browser.views.table'),
    url(r'^browse/(\w+)/(\w+)/table/(\w+)/$', 'browser.views.table'),

    url(r'^browse/(\w+)/(\w+)/query$', 'browser.views.query'),
    url(r'^browse/(\w+)/(\w+)/query/$', 'browser.views.query'),

    url(r'^browse/(\w+)/(\w+)/card/(\w+)$', 'browser.views.card'),
    url(r'^browse/(\w+)/(\w+)/card/(\w+)/$', 'browser.views.card'),

    url(r'^browse/(\w+)/(\w+)/dashboard/(\w+)$', 'browser.views.dashboard'),
    url(r'^browse/(\w+)/(\w+)/dashboard/(\w+)/$', 'browser.views.dashboard'),

    url(r'^browse/(\w+)/(\w+)$', 'browser.views.repo'),
    url(r'^browse/(\w+)/(\w+)/$', 'browser.views.repo'),

    url(r'^browse/(\w+)$', 'browser.views.user'),
    url(r'^browse/(\w+)/$', 'browser.views.user'),
    #### End Browse ####


    ### Delete ####
    url(r'^delete/(\w+)/(\w+)$', 'browser.views.repo_delete'),
    url(r'^delete/(\w+)/(\w+)/$', 'browser.views.repo_delete'),
    
    url(r'^delete/(\w+)/(\w+)/table/(\w+)$', 'browser.views.table_delete'),
    url(r'^delete/(\w+)/(\w+)/table/(\w+)/$', 'browser.views.table_delete'),

    url(r'^delete/(\w+)/(\w+)/card/(\w+)$', 'browser.views.card_delete'),
    url(r'^delete/(\w+)/(\w+)/card/(\w+)/$', 'browser.views.card_delete'),

    url(r'^delete/(\w+)/(\w+)/dashboard/(\w+)$', 'browser.views.dashboard_delete'),
    url(r'^delete/(\w+)/(\w+)/dashboard/(\w+)/$', 'browser.views.dashboard_delete'),
    
    url(r'^delete/(\w+)/(\w+)/file/([\w\d\-\.]+)$', 'browser.views.file_delete'),
    url(r'^delete/(\w+)/(\w+)/file/([\w\d\-\.]+)/$', 'browser.views.file_delete'),
    ### End Delete ####


    ### Export ###
    url(r'^export/(\w+)/(\w+)/table/(\w+)$', 'browser.views.table_export'),
    url(r'^export/(\w+)/(\w+)/table/(\w+)/$', 'browser.views.table_export'),

    url(r'^export/(\w+)/(\w+)/query$', 'browser.views.query_export'),
    url(r'^export/(\w+)/(\w+)/query/$', 'browser.views.query_export'),

    url(r'^export/(\w+)/(\w+)/card/(\w+)$', 'browser.views.card_export'),
    url(r'^export/(\w+)/(\w+)/card/(\w+)/$', 'browser.views.card_export'),
    ### End Export ####

  
    ### Special File Operations ####
    url(r'^upload/(\w+)/(\w+)/file$', 'browser.views.file_upload'),
    url(r'^import/(\w+)/(\w+)/file/([\w\d\-\.]+)', 'browser.views.file_import'),  
    url(r'^download/(\w+)/(\w+)/file/([\w\d\-\.]+)', 'browser.views.file_download'),
    ### End Special File Operations ####


    #### Settings ####
    url(r'^settings/(\w+)/(\w+)$', 'browser.views.repo_settings'),
    url(r'^settings/(\w+)/(\w+)/$', 'browser.views.repo_settings'),

    url(r'^settings/(\w+)$', 'browser.views.user_settings'),
    url(r'^settings/(\w+)/$', 'browser.views.user_settings'),
    #### End Settings ####


    ### Collaborators ###
    url(r'^collaborator/repo/(\w+)/(\w+)/add$', 'browser.views.repo_collaborators_add'),
    url(r'^collaborator/repo/(\w+)/(\w+)/add/$', 'browser.views.repo_collaborators_add'),
    
    url(r'^collaborator/repo/(\w+)/(\w+)/remove/(\w+)$', 'browser.views.repo_collaborators_remove'),
    url(r'^collaborator/repo/(\w+)/(\w+)/remove/(\w+)/$', 'browser.views.repo_collaborators_remove'),
    ### End Collaborators ###


    ### Annotations ####
    url(r'^save-annotation$', 'browser.views.save_annotation'),
    ### End Annotations ####


    #### Apps ####
    url(r'^console$', 'browser.views.console'),
    url(r'^console/$', 'browser.views.console'),

    url(r'^data-refiner/(\w+)/(\w+)$', 'browser.views.data_refiner'),
    url(r'^data-refiner/(\w+)/(\w+)/$', 'browser.views.data_refiner'),

    url(r'^refine-data$', 'browser.views.refine_data'),
    url(r'^refine-data/$', 'browser.views.refine_data'),
    #### End Apps ####


    ### start dbwipes urls ###
    url(r'^dbwipes/(\w+)/(\w+)$', 'browser.views.repo'),
    url(r'^dbwipes/(\w+)/(\w+)/$', 'browser.views.repo'),

    url(r'^dbwipes/(\w+)$', 'browser.views.user'),
    url(r'^dbwipes/(\w+)/$', 'browser.views.user'),

    url(r'^dbwipes/(\w+)/(\w+)/(\w+)$', 'dbwipes.views.index'),
    url(r'^dbwipes/(\w+)/(\w+)/(\w+)/$', 'dbwipes.views.index'),

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