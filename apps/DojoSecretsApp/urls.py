from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^success$', views.success),
    url(r'^secrets$', views.secrets),
    url(r'^new_secret$', views.new_secret),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^like/(?P<id>\d+)$', views.like),
    url(r'^popular$', views.popular),
    url(r'^logout$', views.logout),



]
