# rsvp/admin.py
from django.contrib import admin
from .models import RSVP, Guest

# Inline class for Guests, to show them directly in the RSVP admin
class GuestInline(admin.TabularInline): # Use TabularInline for a compact table layout
    model = Guest
    extra = 0 # Don't show extra empty forms by default
    fields = ['name', 'age', 'dietary_restrictions', 'favorite_song'] # Fields to display for each guest

# Admin class for the RSVP model
class RSVPAdmin(admin.ModelAdmin):
    # Corrected: Using 'submission_date' instead of 'timestamp'
    list_display = ('user', 'is_attending', 'number_of_guests', 'submission_date', 'notes')
    list_filter = ('is_attending', 'submission_date') # Corrected: Using 'submission_date'
    search_fields = ('user__username', 'user__email', 'notes')
    inlines = [GuestInline] # Include the GuestInline here

    # You can also define which fields appear when you ADD/CHANGE an RSVP object
    # For instance:
    # fields = ('user', 'is_attending', 'number_of_guests', 'notes')


# Admin class for the Guest model (optional, as they're often managed via RSVP)
# This allows you to see all guests in a flat list if you need to.
class GuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'rsvp', 'age', 'dietary_restrictions', 'favorite_song')
    list_filter = ('age', 'dietary_restrictions')
    search_fields = ('name', 'rsvp__user__username') # Search by guest name or the associated user's username

# Register your models
admin.site.register(RSVP, RSVPAdmin)
admin.site.register(Guest, GuestAdmin)