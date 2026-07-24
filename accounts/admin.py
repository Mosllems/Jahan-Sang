from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'mobile_number', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Phone Number', {'fields': ('mobile_number',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Phone Number', {'fields': ('mobile_number',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
