# gallery/forms.py
from django import forms
from .models import GalleryImage, Tag

class ImageUploadForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(is_guest_accessible=True), # Filter by new field
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select tags for this photo"
    )
    
    class Meta:
        model = GalleryImage
        fields = ['title', 'description', 'image', 'tags']