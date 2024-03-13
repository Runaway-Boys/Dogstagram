
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import (
    account_view,
    edit_account_view,
)
app_name='accounts'
urlpatterns = [
  path('<user_id>/',account_view,name="view"),
  path('<user_id>/edit/',edit_account_view,name="edit"),
]
