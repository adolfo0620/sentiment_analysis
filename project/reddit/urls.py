from django.conf.urls import patterns, include, url
from django.contrib import admin
from reddit.views import *

urlpatterns = patterns('',
    url(r'^$', Index.as_view() ),
)