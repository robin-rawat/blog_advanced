from django.conf.urls import url
from django.contrib import admin

from . import views


urlpatterns = [
	url(r'^(?P<pk>\d+)/$', views.comment_thread, name="thread" ),
    url(r'^(?P<pk>\d+)/delete/$', views.comment_delete, name="thread_delete"),

]