# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Customize the admin display for CustomUser
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'guest_of')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number', 'guest_of')}),
    )

# Register your CustomUser model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)