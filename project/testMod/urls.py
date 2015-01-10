from django.conf.urls import patterns, include, url
from django.contrib import admin
from testMod.views import *

urlpatterns = patterns('',
    url(r'^$', Index.as_view()),

)
