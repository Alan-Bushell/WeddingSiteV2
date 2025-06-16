# rsvp/models.py
from django.db import models
from django.conf import settings

class RSVP(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rsvp_submission'
    )
    is_attending = models.BooleanField(default=True, verbose_name="Will you be attending?")
    number_of_guests = models.PositiveIntegerField(
        default=1,
        help_text="Including yourself, how many people will be in your party?",
        verbose_name="Number in Party"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Any additional notes or messages for the couple.",
        verbose_name="Additional Notes"
    )
    submission_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "RSVP"
        verbose_name_plural = "RSVPs"

    def __str__(self):
        return f"RSVP by {self.user.username} - Attending: {self.is_attending}"

class Guest(models.Model):
    # ... (this model stays the same)
    rsvp = models.ForeignKey(
        RSVP,
        on_delete=models.CASCADE,
        related_name='guests'
    )
    name = models.CharField(max_length=100, verbose_name="Guest Name")
    age = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Optional: For meal planning (e.g., child meal).",
        verbose_name="Guest Age"
    )
    dietary_restrictions = models.TextField(
        blank=True,
        null=True,
        help_text="e.g., Vegetarian, Gluten-free, Nut allergy",
        verbose_name="Dietary Restrictions"
    )
    favorite_song = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="What song would get this guest on the dance floor?",
        verbose_name="Favorite Song"
    )

    class Meta:
        verbose_name = "Guest"
        verbose_name_plural = "Guests"
        ordering = ['name']

    def __str__(self):
        return self.name