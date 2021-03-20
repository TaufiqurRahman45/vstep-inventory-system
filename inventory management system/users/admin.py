from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_operation', 'is_supplier', 'is_admin', 'is_ppc']


admin.site.register(User, UserAdmin)
