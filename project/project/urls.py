from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^twit/', include('twit.urls')),
    url(r'^$', include('users.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^testmod/', include('testMod.urls')),
    url(r'^tumblr/', include('tumblr.urls')),
)
