# rsvp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.rsvp_submission_view, name='rsvp'),
    path('success/', views.rsvp_success_view, name='rsvp_success'),
]