# gallery/models.py
from django.db import models

class GalleryImage(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, help_text="A short title for the image (optional)")
    image = models.ImageField(upload_to='gallery_images/') # Images will be stored in MEDIA_ROOT/gallery_images/
    description = models.TextField(blank=True, null=True, help_text="A brief description of the image (optional)")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False, help_text="Check to feature this image on the homepage or elsewhere.")

    class Meta:
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"
        ordering = ['-uploaded_at'] # Order by newest images first

    def __str__(self):
        return self.title if self.title else f"Image {self.id}"