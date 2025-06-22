# gallery/views.py
from django.shortcuts import render
from .models import GalleryImage # Import your new model

def gallery_view(request):
    """
    Renders the gallery page with all uploaded images.
    """
    images = GalleryImage.objects.all() # Fetch all images from the database, ordered by 'uploaded_at' due to Meta class
    context = {
        'images': images # Pass the list of images to the template
    }
    return render(request, 'gallery/gallery.html', context)