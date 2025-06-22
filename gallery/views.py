# gallery/views.py
from django.shortcuts import render

def gallery_view(request):
    """
    Renders the gallery page.
    """
    # For now, we'll just pass an empty context.
    # Later, you'd fetch actual image data here.
    context = {
        'images': [] # Placeholder for image data
    }
    return render(request, 'gallery/gallery.html', context)