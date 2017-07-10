from django.conf.urls import url, include
from cast import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^tags/$', views.tagged_list, name='tagged_list'),
    url(r'^contents/(?P<contents_pk>\d+)/$', views.contents_detail, name='contents_detail'),
    url(r'^congressman/(?P<congressman_pk>\d+)/$', views.congressman_detail, name='congressman_detail'),
    url(r'^pledge/(?P<pledge_pk>\d+)/$', views.pledge_detail, name='pledge_detail'),
    url(r'^contents-emotion/(?P<contents_pk>\d+)/$', views.contents_emotion, name='contents_emotion'),
    url(r'^pledge-emotion/(?P<pledge_pk>\d+)/$', views.pledge_emotion, name='pledge_emotion'),
    url(r'^congressman-emotion/(?P<congressman_pk>\d+)/$', views.congressman_emotion, name='congressman_emotion'),
    url(r'^(?P<pk>\d+)/comment/new/$', views.comment_new, name='comment_new'),
    url(r'^comment/(?P<comment_pk>\d+)/edit/$', views.comment_edit, name='comment_edit'),
    url(r'^comment/(?P<comment_pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),
    url(r'^comment-emotion/(?P<comment_pk>\d+)/$', views.comment_emotion, name='comment_emotion'),
    url(r'^(?P<comment_pk>\d+)/recomment/new/$', views.recomment_new, name='recomment_new'),
    url(r'^recomment/(?P<recomment_pk>\d+)/delete/$', views.recomment_delete, name='recomment_delete'),
    url(r'^ajax/tag/autocomplete/$', views.ajax_tag_autocomplete, name='ajax_tag_autocomplete'),
    url(r'^ajax/favorites/(?P<pk>\d+)/$', views.ajax_favorites, name='ajax_favorites'),


]
