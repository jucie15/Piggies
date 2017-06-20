from django.conf.urls import url, include
from django.contrib import admin
from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^signup-info/$', views.signup_info, name='signup_info'),
    url(r'^set-tag/$', views.set_tag, name='set_tag'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^logout/$', auth_views.logout, name='logout', kwargs={'next_page': 'cast:index'}),
]
