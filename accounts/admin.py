from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import DogAccount


class AccountAdmin(UserAdmin):
    list_display = ('email','username','date_joined','is_admin','is_staff')
    search_fields = ('email','username')
    readonly_fields = ('id','date_joined','last_login')
    filter_horizontal=()
    list_filter=()
    fieldsets=()
admin.site.register(DogAccount,AccountAdmin)