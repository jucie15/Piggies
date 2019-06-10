from django.urls import path
from board import views

app_name = 'board'

urlpatterns = [
    path('feedback/', views.feedback_list, name='feedback_list'),
    path('feedback/<int:feedback_pk>/', views.feedback_detail, name='feedback_detail'),
    path('feedback/new/', views.feedback_new, name='feedback_new'),
    path('feedback/edit/<int:feedback_pk>/', views.feedback_edit, name='feedback_edit'),
    path('feedback/delete/<int:feedback_pk>/', views.feedback_delete, name='feedback_delete'),
    path('post/', views.post_list, name='post_list'),
    path('<int:pk>/comment/new/', views.comment_new, name='comment_new'),
    path('comment/<int:comment_pk>/edit/', views.comment_edit, name='comment_edit'),
    path('comment/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
]



