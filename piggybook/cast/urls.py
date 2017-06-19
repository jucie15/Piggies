from django.conf.urls import url, include
from cast import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^tagged-contents/$', views.tagged_list, name='tagged_list'),
]
