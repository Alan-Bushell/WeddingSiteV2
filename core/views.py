# wedding_project/core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from articles.models import Article
from gallery.models import GalleryImage

def home_view(request):
    # --- Data for sections ---
    try:
        # Retrieve the 3 most recent, published articles
        latest_articles = Article.objects.filter(is_published=True).order_by('-published_date')[:3]
    except Exception as e:
        print(f"Error fetching latest articles: {e}")
        latest_articles = []
    
    # Retrieve up to 8 images that are both public and featured
    try:
        featured_images = GalleryImage.objects.filter(is_public=True, is_featured=True)[:8]
    except Exception as e:
        print(f"Error fetching featured images: {e}")
        featured_images = []

    # Split the list into two halves to prevent duplication
    gallery_photos_top = featured_images[:4]
    gallery_photos_bottom = featured_images[4:]

    # -------------------------------------------------------------

    context = {
        'latest_articles': latest_articles,
        'gallery_photos_top': gallery_photos_top,
        'gallery_photos_bottom': gallery_photos_bottom,
        'wedding_date': 'October 31, 2026', # Hardcoded for now
        'wedding_location': 'Cape Panwa Hotel, Phuket, Thailand', # Hardcoded for now
        'map_embed_url': 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3066.2890155982077!2d98.40821513707338!3d7.807672204988176!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x30502c170a4c1303%3A0xac18e439e9c17960!2sCape%20Panwa%20Hotel!5e1!3m2!1sen!2sie!4v1750613331257!5m2!1sen!2sie"',
        'week1_days': ["19", "20", "21", "22", "23", "24", "25"],
        'week2_days': ["26", "27", "28", "29", "30"],
        'calendar_days': [1, 2, 3, 4, 5, 6, 7],  # <-- This must be present!
        'carousel_imgs': ["left_1.jpg", "left_2.jpg", "left_3.jpg", "left_4.jpg"],
    }
    return render(request, 'core/home.html', context)

# new home view

def home_view2(request):
    # --- Data for sections ---
    try:
        # Retrieve the 3 most recent, published articles
        latest_articles = Article.objects.filter(is_published=True).order_by('-published_date')[:3]
    except Exception as e:
        print(f"Error fetching latest articles: {e}")
        latest_articles = []
    
    # Retrieve up to 8 images that are both public and featured
    try:
        featured_images = GalleryImage.objects.filter(is_public=True, is_featured=True)[:8]
    except Exception as e:
        print(f"Error fetching featured images: {e}")
        featured_images = []

    # Split the list into two halves to prevent duplication
    gallery_photos_top = featured_images[:4]
    gallery_photos_bottom = featured_images[4:]

    # -------------------------------------------------------------

    context = {
        'latest_articles': latest_articles,
        'gallery_photos_top': gallery_photos_top,
        'gallery_photos_bottom': gallery_photos_bottom,
        'wedding_date': 'October 31, 2026', # Hardcoded for now
        'wedding_location': 'Cape Panwa Hotel, Phuket, Thailand', # Hardcoded for now
        'map_embed_url': 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3066.2890155982077!2d98.40821513707338!3d7.807672204988176!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x30502c170a4c1303%3A0xac18e439e9c17960!2sCape%20Panwa%20Hotel!5e1!3m2!1sen!2sie!4v1750613331257!5m2!1sen!2sie"',
    }
    return render(request, 'core/home2.html', context)


# Custom 404 (Page Not Found) View
def custom_404(request, exception):
    return render(request, 'core/404.html', status=404)

# Custom 500 (Server Error) View
def custom_500(request, *args, **kwargs):
    return render(request, 'core/500.html', status=500)