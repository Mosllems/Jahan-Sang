from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Profile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'mobile_number', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Phone Number', {'fields': ('mobile_number',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Phone Number', {'fields': ('mobile_number',)}),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'username', 'mobile_number']
    search_fields = ['user__username', 'user__email', 'user__mobile_number']
    list_filter = ['user__is_staff', 'user__is_active']
    readonly_fields = ['user',]

    @admin.display(description='Username')
    def username(self, obj):
        return obj.user.username

    @admin.display(description='Mobile Number')
    def mobile_number(self, obj):
        return obj.user.mobile_number