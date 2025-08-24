# gallery/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery_view, name='gallery'),
    path('tag/<slug:tag_slug>/', views.gallery_view, name='gallery_by_tag'),
    path('upload/', views.upload_image_view, name='upload_image'),
]