from django.conf.urls import patterns, include, url
from django.contrib import admin
from facebook.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', login_required( Index.as_view() ), name="index" ),
    url(r'^callback', Callback.as_view()),
    url(r'^eval', login_required( Eval.as_view() ), name="eval" ),
    url(r'^results', Results.as_view()),
)
