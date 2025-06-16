# rsvp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.rsvp_submission_view, name='rsvp_submission'),
    path('success/', views.rsvp_success_view, name='rsvp_success'),
]