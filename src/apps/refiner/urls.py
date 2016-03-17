from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^$', 'refiner.views.index'),
    url(r'^refine-data$', 'refiner.views.refine_data'),
    url(r'^api/v1/refiner$', views.Refiner.as_view()),
)
