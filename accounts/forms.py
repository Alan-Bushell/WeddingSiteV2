# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    A custom form for creating new CustomUser instances.
    Extends Django's built-in UserCreationForm to include custom fields.
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('phone_number',) # Add custom fields here

class UserProfileForm(UserChangeForm):
    """
    A form for updating existing CustomUser instances.
    Note: password fields are excluded as they are handled separately.
    """
    password = None # Exclude password field from direct editing here

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number',) # Fields you want to allow editing
        # You might want to remove 'username' or 'email' if you don't want users changing them
        # For this example, we include them.