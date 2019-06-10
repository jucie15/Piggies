from django.urls import path
from django.contrib import admin
from accounts import views
from django.contrib.auth import logout

app_name = 'account'

urlpatterns = [
    path('signup-info/', views.signup_info, name='signup_info'),
    path('set-tag/', views.set_tag, name='set_tag'),
    path('ajax/add/tag/', views.ajax_add_tag, name='ajax_add_tag'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('logout/', logout, name='logout', kwargs={'next_page': 'cast:index'}),
    path('tag_delete/', views.tag_delete, name='tag_delete'),
]
