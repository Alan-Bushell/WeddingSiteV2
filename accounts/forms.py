# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm as BaseUserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    A custom form for creating new CustomUser instances.
    Extends Django's built-in UserCreationForm to include custom fields.
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # keeps default UserCreationForm fields (e.g., username) + your custom field
        fields = UserCreationForm.Meta.fields + ('phone_number',)

class UserProfileForm(BaseUserChangeForm):
    """
    Front-end profile form (optional). Excludes password field.
    """
    password = None

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number',)

# Admin change form: safe and complete
class CustomUserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        model = CustomUser
        fields = "__all__"