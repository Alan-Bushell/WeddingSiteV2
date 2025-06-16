# rsvp/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import RSVP, Guest

class RSVPForm(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = ['is_attending', 'number_of_guests', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['name', 'age', 'dietary_restrictions', 'favorite_song']
        widgets = {
            'dietary_restrictions': forms.Textarea(attrs={'rows': 2}),
        }

# This creates a formset for managing multiple Guest instances related to an RSVP
GuestFormSet = inlineformset_factory(
    RSVP,
    Guest,
    form=GuestForm,
    extra=1,  # Number of empty forms to display initially
    can_delete=True, # Allow deleting existing guest forms
    max_num=10 # Maximum number of guest forms allowed
)