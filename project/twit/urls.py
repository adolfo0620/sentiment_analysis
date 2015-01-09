from django.conf.urls import patterns, include, url
from django.contrib import admin
from twit.views import *

urlpatterns = patterns('',
    url(r'^$', Index.as_view()),
    url(r'^callback', Callback.as_view()),
    url(r'^tweet', Tweet.as_view()),
    url(r'^eval', Eval.as_view()),
    url(r'^results', Results.as_view()),
)
