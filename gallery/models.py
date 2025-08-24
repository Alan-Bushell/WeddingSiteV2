# gallery/models.py
from django.db import models
from django.conf import settings # Import settings to reference the user model
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    is_published = models.BooleanField(default=True, help_text="Uncheck to hide this tag from the gallery filters.")
    is_guest_accessible = models.BooleanField(default=False, help_text="Check to make this tag available for guests to select when uploading photos.")

    def __str__(self):
        return self.name

class GalleryImage(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, help_text="A short title for the image (optional)")
    image = models.ImageField(upload_to='gallery_images/')
    description = models.TextField(blank=True, null=True, help_text="A brief description of the image (optional)")
    tags = models.ManyToManyField(Tag, blank=True, related_name='images')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False, help_text="Check to feature this image on the homepage or elsewhere.")
    contributor = models.ForeignKey( # New Field
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name='uploaded_images'
    )
    is_public = models.BooleanField( # New Field
        default=False, 
        help_text="Check to display this image in the public gallery."
    )

    class Meta:
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title if self.title else f"Image {self.id}"