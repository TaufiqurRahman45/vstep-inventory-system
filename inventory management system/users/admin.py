from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'is_operation', 'is_admin', 'is_ppc']


admin.site.register(User, UserAdmin)
