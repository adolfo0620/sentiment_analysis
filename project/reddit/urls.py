from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from reddit.views import *

urlpatterns = patterns('',
    url(r'^$', Index.as_view() ),
    url(r'^eval', login_required( Eval.as_view() ), name="eval" ),
)