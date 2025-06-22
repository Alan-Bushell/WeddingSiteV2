# articles/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.articles_view, name='articles'), # This defines the root for the 'articles' app and names it 'articles'
]