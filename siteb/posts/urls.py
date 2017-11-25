from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
	url(r'^$', views.post_home, name="home" ),
	url(r'^create/$', views.post_create, name="create"),
	url(r'^detail/(?P<pk>\d+)/$', views.post_detail, name="detail" ),
	url(r'^list/$', views.post_list, name="list" ),
	url(r'^(?P<pk>\d+)/edit/$', views.post_update, name="update" ),
    url(r'^(?P<pk>\d+)/delete/$', views.post_delete, name="delete"),

]
