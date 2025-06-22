# core/views.py
from django.shortcuts import render

def home_view(request):
    """
    Renders the homepage.
    """
    return render(request, 'core/home.html')