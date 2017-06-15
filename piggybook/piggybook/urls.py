from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'$', include('cast.urls', namespace='cast')), #처음에 r'$' 공백페이지를 연결하는 코드 없어서 임시로 추가함.
    url(r'^admin/', admin.site.urls),
    url(r'^cast/', include('cast.urls', namespace='cast')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^accounts/', include('allauth.urls')),
]
