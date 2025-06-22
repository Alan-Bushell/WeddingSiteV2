# wedding_project/core/views.py
from django.shortcuts import render
# from articles.models import Article # Uncomment this line in a future step
# from gallery.models import Photo   # Uncomment this line in a future step

def home_view(request):
    # --- Data for sections (will be populated from models later) ---
    latest_articles = [] # Placeholder: Will fetch from Article model
    gallery_photos_top = [] # Placeholder: Will fetch from Photo model
    gallery_photos_bottom = [] # Placeholder: Will fetch from Photo model

    # Example: To fetch data when models are ready, you'd uncomment these:
    # try:
    #     latest_articles = Article.objects.order_by('-publish_date')[:3]
    # except:
    #     pass # Handle case where Article model/data doesn't exist yet

    # try:
    #     gallery_photos_top = Photo.objects.all().order_by('?')[:4]
    #     gallery_photos_bottom = Photo.objects.all().order_by('?')[:4]
    # except:
    #     pass # Handle case where Photo model/data doesn't exist yet
    # -------------------------------------------------------------

    context = {
        'latest_articles': latest_articles,
        'gallery_photos_top': gallery_photos_top,
        'gallery_photos_bottom': gallery_photos_bottom,
        'wedding_date': 'October 31, 2026', # Hardcoded for now
        'wedding_location': 'Cape Panwa Hotel, Phuket, Thailand', # Hardcoded for now
        'map_embed_url': 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3066.2890155982077!2d98.40821513707338!3d7.807672204988176!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x30502c170a4c1303%3A0xac18e439e9c17960!2sCape%20Panwa%20Hotel!5e1!3m2!1sen!2sie!4v1750613331257!5m2!1sen!2sie"',
    }
    return render(request, 'core/home.html', context)