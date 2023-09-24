
from django.urls import path

from .views import (
    register_view,
    login_view,
    index,
    
    
    )




app_name='accounts'
urlpatterns = [
    path("",index,name = 'index'),
    path("register/",register_view,name = 'register'),
    path("login/",login_view,name = 'login'),
]