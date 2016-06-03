from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'refiner.views.index'),
    url(r'^refine-data$', 'refiner.views.refine_data'),
    url(r'^create-table$', 'refiner.views.create_table')
)