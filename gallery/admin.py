# gallery/admin.py
from django.contrib import admin
from .models import GalleryImage # Import your new model

@admin.register(GalleryImage) # This decorator registers the model with the admin site
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'uploaded_at', 'is_featured')
    list_filter = ('is_featured', 'uploaded_at')
    search_fields = ('title', 'description')
    #  add more customization here later, e.g., showing a thumbnail