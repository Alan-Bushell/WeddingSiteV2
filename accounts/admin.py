# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    # Be tolerant to differing fields across CustomUser variants
    def get_list_display(self, request):
        names = {f.name for f in self.model._meta.get_fields()}
        cols = []
        for field in ("username", "email", "first_name", "last_name"):
            if field in names:
                cols.append(field)
        cols.append("is_staff")
        return tuple(cols)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        names = {f.name for f in self.model._meta.get_fields()}
        extra = [f for f in ("phone_number", "guest_of") if f in names]
        if extra:
            fieldsets = fieldsets + ((_("Profile"), {"fields": tuple(extra)}),)
        return fieldsets

    def get_add_fieldsets(self, request):
        fieldsets = super().get_add_fieldsets(request)
        names = {f.name for f in self.model._meta.get_fields()}
        extra = [f for f in ("phone_number", "guest_of") if f in names]
        if extra:
            fieldsets = fieldsets + ((_("Profile"), {"fields": tuple(extra)}),)
        return fieldsets

admin.site.register(CustomUser, CustomUserAdmin)