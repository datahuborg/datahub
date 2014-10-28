from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^login', 'browser.auth.login'),
    url(r'^register', 'browser.auth.register'),
    url(r'^logout', 'browser.auth.logout'),

    url(r'^forgot', 'browser.auth.forgot'),
    url(r'^reset/(\w+)', 'browser.auth.reset'),
    url(r'^verify/(\w+)', 'browser.auth.verify'),

    url(r'^$', 'browser.views.home'),
    url(r'^about$', 'browser.views.about'),
    url(r'^team$', 'browser.views.team'),
    url(r'^developer$', 'browser.views.developer_apis'),
    url(r'^developer/$', 'browser.views.developer_apis'),
    url(r'^developer/apis$', 'browser.views.developer_apis'),
    url(r'^developer/apps$', 'browser.views.developer_apps'),

    url(r'^console$', 'browser.views.console'),
    url(r'^console/$', 'browser.views.console'),

    url(r'^visualize$', 'browser.views.visualize'),
    url(r'^visualize/$', 'browser.views.visualize'),

    url(r'^newrepo/(\w+)$', 'browser.views.newrepo'),
    url(r'^newrepo/(\w+)/$', 'browser.views.newrepo'),

    url(r'^data-refiner/(\w+)/(\w+)$', 'browser.views.data_refiner'),
    url(r'^data-refiner/(\w+)/(\w+)/$', 'browser.views.data_refiner'),

    url(r'^refine-data$', 'browser.views.refine_data'),
    url(r'^refine-data/$', 'browser.views.refine_data'),

    url(r'^handle-file-upload$', 'browser.views.handle_file_upload'),

    url(r'^add-collaborator/(\w+)/(\w+)$', 'browser.views.add_collaborator'),
    url(r'^delete-collaborator/(\w+)/(\w+)/(\w+)$', 'browser.views.delete_collaborator'),

    url(r'^import/(\w+)/(\w+)', 'browser.views.file_import'),
    url(r'^delete/(\w+)/(\w+)', 'browser.views.file_delete'),
    url(r'^download/(\w+)/(\w+)', 'browser.views.file_download'),
    url(r'^export/(\w+)/(\w+)/(\w+)', 'browser.views.file_export'),

    url(r'^delete-table/(\w+)/(\w+)/(\w+)', 'browser.views.table_delete'),
    url(r'^delete-repo/(\w+)/(\w+)', 'browser.views.repo_delete'),

    url(r'^service$', 'browser.views.service_binary'),
    url(r'^service/binary$', 'browser.views.service_binary'),
    url(r'^service/json$', 'browser.views.service_json'),

    url(r'^browse/(\w+)/(\w+)/(\w+)$', 'browser.views.table'),
    url(r'^browse/(\w+)/(\w+)/(\w+)/(\w+)$', 'browser.views.table'),
    url(r'^browse/(\w+)/(\w+)/(\w+)/(\w+)/$', 'browser.views.table'),

    url(r'^browse/(\w+)/(\w+)$', 'browser.views.repo'),
    url(r'^browse/(\w+)/(\w+)/$', 'browser.views.repo'),

    url(r'^browse/(\w+)$', 'browser.views.user'),
    url(r'^browse/(\w+)/$', 'browser.views.user'),

    url(r'^settings/(\w+)/(\w+)/(\w+)$', 'browser.views.settings_table'),
    url(r'^settings/(\w+)/(\w+)/(\w+)/(\w+)$', 'browser.views.settings_table'),
    url(r'^settings/(\w+)/(\w+)/(\w+)/(\w+)/$', 'browser.views.settings_table'),

    url(r'^settings/(\w+)/(\w+)$', 'browser.views.settings_repo'),
    url(r'^settings/(\w+)/(\w+)/$', 'browser.views.settings_repo'),

    url(r'^settings/(\w+)$', 'browser.views.settings_database'),
    url(r'^settings/(\w+)/$', 'browser.views.settings_database'),


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

    ### start web-page urls ###

    url(r'^about$', 'www.views.home'),
    url(r'^about/$', 'www.views.home'),
    url(r'^about/team$', 'www.views.team')
)