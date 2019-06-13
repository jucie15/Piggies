from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin
from cast import views


urlpatterns = [
    path('', views.index), #처음에 r'$' 공백페이지를 연결하는 코드 없어서 임시로 추가함.
    path('admin/', admin.site.urls),
    path('cast/', include('cast.urls', namespace='cast')),
    path('board/', include('board.urls', namespace='board')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('accounts/', include('allauth.urls')),
    #comment edit ajax
    path('comment/edit/<int:comment_pk>/', views.comment_editform),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)), ]
