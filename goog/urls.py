from django.conf.urls import patterns, include, url
from django.contrib import admin
from goog.views import *

urlpatterns = patterns('',
    url(r'^$', Index.as_view() ),
    url(r'^callback', Callback.as_view()),
    url(r'^display', Display.as_view()),
)
