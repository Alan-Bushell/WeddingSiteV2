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

class UserProfileForm(UserChangeForm): # Your existing form
    """
    A form for updating existing CustomUser instances.
    Note: password fields are excluded as they are handled separately.
    """
    password = None # Exclude password field from direct editing here

    class Meta:
        model = CustomUser
        # Adjust fields: include first_name, last_name, and phone_number
        # Consider if you want 'username' to be directly editable by the user.
        # Often, username is not editable on a profile, while first/last/email are.
        fields = ('first_name', 'last_name', 'email', 'phone_number',) # <--- MODIFIED FIELDS HERE
        # You might want to remove 'username' or 'email' if you don't want users changing them
        # For this example, we include them.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap form-control class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'