
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import (
    register_view,
    login_view,
    logout_view,
    upload,
    index
    )



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  index,name="index"),
    path("register/",register_view,name = 'register'),
    path("login/",login_view,name = 'login'),
    path("logout/",logout_view,name = 'logout'),
    path("upload/",upload,name = 'upload'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)