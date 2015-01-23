from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from users.views import *

urlpatterns = patterns('',
    url( r'^$', Index.as_view() ),
    url( r'^signup$', Signup.as_view() ),
    url( r'^login$', Login.as_view() ),
    url( r'^logout$', Logout.as_view() ),
    url( r'^profile$', login_required( Profile.as_view() ), name="profile" ),
    url( r'^changepassword$', login_required( ChangePassword.as_view() ), name="changePassword" ),
)
