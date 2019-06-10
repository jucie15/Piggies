from django.urls import path
from cast import views

app_name = 'cast'

urlpatterns = [
    path('', views.index, name='index'),
    path('pledge_list/', views.pledge_list, name='pledge_list'),
    path('congressman_list/', views.congressman_list, name='congressman_list'),
    path('tags/', views.tagged_list, name='tagged_list'),
    path('contents/<int:contents_pk>/', views.contents_detail, name='contents_detail'),
    path('congressman/<int:congressman_pk>/', views.congressman_detail, name='congressman_detail'),
    path('pledge/<int:pledge_pk>/', views.pledge_detail, name='pledge_detail'),
    path('contents-emotion/<int:contents_pk>/', views.contents_emotion, name='contents_emotion'),
    path('pledge-emotion/<int:pledge_pk>/', views.pledge_emotion, name='pledge_emotion'),
    path('congressman-emotion/<int:congressman_pk>/', views.congressman_emotion, name='congressman_emotion'),
    path('<int:pk>/comment/', views.comment_list, name='comment_list'),
    path('<int:pk>/comment/new/', views.comment_new, name='comment_new'),
    path('comment/<int:comment_pk>/edit/', views.comment_edit, name='comment_edit'),
    path('comment/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('comment-emotion/<int:comment_pk>/', views.comment_emotion, name='comment_emotion'),
    path('<int:comment_pk>/recomment/new/', views.recomment_new, name='recomment_new'),
    path('recomment/<int:recomment_pk>/delete/', views.recomment_delete, name='recomment_delete'),
    path('ajax/tag/autocomplete/', views.ajax_tag_autocomplete, name='ajax_tag_autocomplete'),
    path('ajax/favorites/<int:pk>/', views.ajax_favorites, name='ajax_favorites'),
    path('ajax/add/tag/<int:pk>/', views.ajax_add_tag, name='ajax_add_tag'),
]
