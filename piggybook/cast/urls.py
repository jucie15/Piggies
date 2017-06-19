from django.conf.urls import url, include
from cast import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^tagged/$', views.tagged_list, name='tagged_list'),
    url(r'^contents/(?P<contents_pk>\d+)/$', views.contents_detail, name='contents_detail'),
    url(r'^congressman/(?P<cm_pk>\d+)/$', views.congressman_detail, name='congressman_detail'),
    url(r'^pledge_detail/(?P<pledge_pk>\d+)/$', views.pledge_detail, name='pledge_detail'),

]
