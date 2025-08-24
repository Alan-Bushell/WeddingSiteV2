# gallery/admin.py
from django.contrib import admin
from .models import GalleryImage, Tag # Import both models

# Register the Tag model
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_published', 'is_guest_accessible')
    list_editable = ('is_published', 'is_guest_accessible')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    # ADDED 'is_public' to list_display and list_editable
    list_display = ('title', 'is_public', 'is_featured', 'uploaded_at', 'display_tags')
    list_editable = ('is_public', 'is_featured')
    list_filter = ('is_public', 'is_featured', 'tags')
    search_fields = ('title', 'description')
    date_hierarchy = 'uploaded_at'
    readonly_fields = ('uploaded_at',)

    fieldsets = (
        (None, {
            'fields': ('title', 'image', 'description', 'tags')
        }),
        ('Display Options', {
            'fields': ('is_public', 'is_featured',),
            'classes': ('collapse',)
        }),
    )

    def display_tags(self, obj):
        """Creates a comma-separated string of tags for list display"""
        return ", ".join([tag.name for tag in obj.tags.all()])
    
    display_tags.short_description = 'Tags'