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
        # Optional: Add labels and help_texts here for better UX (as previously suggested)
        # labels = {
        #     'is_attending': "Will you be attending?",
        #     'number_of_guests': "Including yourself, how many people will be in your party?",
        #     'notes': "Additional Notes",
        # }
        # help_texts = {
        #     'number_of_guests': "Enter the total number of adults and children in your party, including yourself. If attending alone, enter 1.",
        # }


class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['name', 'age', 'dietary_restrictions', 'favorite_song']
        widgets = {
            'dietary_restrictions': forms.Textarea(attrs={'rows': 2}),
        }
        # Optional: Add labels and help_texts here for better UX (as previously suggested)
        # labels = {
        #     'name': "Guest Name",
        #     'age': "Guest Age",
        #     'dietary_restrictions': "Dietary Restrictions",
        #     'favorite_song': "Favorite Song",
        # }
        # help_texts = {
        #     'age': "Optional: For meal planning (e.g., child meal).",
        #     'dietary_restrictions': "e.g., Vegetarian, Gluten-free, Nut allergy",
        #     'favorite_song': "What song would get this guest on the dance floor?",
        # }

    # Add this clean method for sanitization
    def clean_favorite_song(self):
        song = self.cleaned_data.get('favorite_song')
        if song:
            song = song.strip()
            song = song.title()
            song = ' '.join(song.split())
        return song

# This creates a formset for managing multiple Guest instances related to an RSVP
GuestFormSet = inlineformset_factory(
    RSVP,
    Guest,
    form=GuestForm,
    can_delete=True,
    max_num=10,
    min_num=0,
    validate_min=False
)