# articles/views.py
from django.shortcuts import render

def articles_view(request):
    """
    Renders the 'Our Story' or articles page.
    """
    # For now, we'll just pass an empty context.
    # Later, you might fetch blog posts or story sections here.
    context = {
        'articles': [] # Placeholder for article data
    }
    return render(request, 'articles/articles.html', context)