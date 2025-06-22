# gallery/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery_view, name='gallery'), # This defines the root for the 'gallery' app and names it 'gallery'
]