# articles/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list_view, name='article_list'), # URL for listing all articles
    path('<slug:slug>/', views.article_detail_view, name='article_detail'), # URL for a single article
]