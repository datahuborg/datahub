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

    url(r'^data-refiner$', 'browser.views.data_refiner'),
    url(r'^data-refiner/$', 'browser.views.data_refiner'),

    url(r'^refine-data$', 'browser.views.refine_data'),
    url(r'^refine-data/$', 'browser.views.refine_data'),

    url(r'^files/(\w+)/(\w+)$', 'browser.views.files'),
    url(r'^files/(\w+)/(\w+)/$', 'browser.views.files'),

    url(r'^handle-file-upload$', 'browser.views.handle_file_upload'),

    url(r'^create_table_from_file$', 'browser.views.create_table_from_file'),
    url(r'^create-table-from-file-data$', 'browser.views.create_table_from_file_data'),

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
    url(r'^api/scorpion/$', 'dbwipes.views.scorpion')

)