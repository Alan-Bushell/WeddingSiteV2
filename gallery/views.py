# gallery/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import GalleryImage, Tag # Import all models
from .forms import ImageUploadForm # Import the new form

def gallery_view(request, tag_slug=None):
    """
    Renders the gallery page, optionally filtered by a tag.
    """
    images = GalleryImage.objects.filter(is_public=True) # Only show public images
    # Fetch only published tags
    tags = Tag.objects.filter(is_published=True)

    if tag_slug:
        # Filter images by the selected tag
        tag = Tag.objects.get(slug=tag_slug)
        images = images.filter(tags=tag)

    context = {
        'images': images,
        'tags': tags,
        'active_tag': tag_slug,
    }
    return render(request, 'gallery/gallery.html', context)

# New view for uploading images
@login_required
def upload_image_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.contributor = request.user
            image.is_public = False # Images require admin approval before being public
            image.save()
            form.save_m2m() # Save the many-to-many relationship for tags
            return redirect('gallery') # Redirect to the gallery page after upload
    else:
        form = ImageUploadForm()
    
    context = {'form': form}
    return render(request, 'gallery/upload_image.html', context)