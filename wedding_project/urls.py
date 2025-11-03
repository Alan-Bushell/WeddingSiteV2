# wedding_project/urls.py
from django.contrib import admin
from django.urls import path, include 
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')), 
    path('rsvp/', include('rsvp.urls')),
    path('gallery/', include('gallery.urls')),
    path('articles/', include('articles.urls')),
    path('details/', TemplateView.as_view(template_name='core/wedding_details.html'), name='wedding_details'),
    path('', include('core.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# --- NEW: CUSTOM ERROR HANDLERS ---
handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'
# ----------------------------------