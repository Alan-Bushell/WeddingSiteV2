# articles/views.py
from django.shortcuts import render, get_object_or_404
from .models import Article # Make sure Article is imported

def article_list_view(request):
    """
    Displays a list of all published articles, ordered by publication date.
    """
    articles = Article.objects.filter(is_published=True).order_by('-published_date')
    context = {
        'articles': articles
    }
    return render(request, 'articles/article_list.html', context)

def article_detail_view(request, slug):
    """
    Displays a single article based on its slug.
    Returns a 404 error if the article is not found or not published.
    """
    article = get_object_or_404(Article, slug=slug, is_published=True)
    context = {
        'article': article
    }
    return render(request, 'articles/article_detail.html', context)