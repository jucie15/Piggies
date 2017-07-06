from django.conf.urls import url
from board import views

urlpatterns = [
    url(r'^feedback/$', views.feedback_list, name='feedback_list'),
    url(r'^feedback/(?P<feedback_pk>\d+)/$', views.feedback_detail, name='feedback_detail'),
    url(r'^feedback/new/$', views.feedback_new, name='feedback_new'),
    url(r'^feedback/edit/(?P<feedback_pk>\d+)/$', views.feedback_edit, name='feedback_edit'),
    url(r'^feedback/delete/(?P<feedback_pk>\d+)/$', views.feedback_delete, name='feedback_delete'),
    url(r'^post/$', views.post_list, name='post_list'),
    url(r'^(?P<pk>\d+)/comment/new/$', views.comment_new, name='comment_new'),
    url(r'^comment/(?P<comment_pk>\d+)/edit/$', views.comment_edit, name='comment_edit'),
    url(r'^comment/(?P<comment_pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),
]


