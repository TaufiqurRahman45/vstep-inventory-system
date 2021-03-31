from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'is_operation', 'is_admin', 'is_ppc']
    fieldsets = (
        ('User', {'fields': ('username', 'password')}),
        ('Personal Information', {'fields': (
            'first_name',
            'last_name',
            'email',
        )}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'is_operation',
            'is_admin',
            'is_ppc',
        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser',
                'is_operation',
                'is_admin',
                'is_ppc',),
        }),
    )


admin.site.register(User, UserAdmin)
