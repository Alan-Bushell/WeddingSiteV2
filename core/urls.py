# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'), # This defines the root for the 'core' app
    path('home2', views.home_view2, name='home2'), 
]