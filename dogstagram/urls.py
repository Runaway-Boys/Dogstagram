
from django.contrib import admin
from django.urls import path,include

from accounts.views import (
    register_view,
    login_view
    )



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  include('accounts.urls')),
]
