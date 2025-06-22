# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views # Import Django's built-in auth views
from . import views # Import your custom views from accounts/views.py

urlpatterns = [
    # Django's built-in authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'), # Redirects to login page after logout

    # Password Reset URLs (Django provides these out of the box)
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    # Your custom account-related URLs (placeholders for now)
    # You will create these views/templates next, but the URLs can be here
    path('signup/', views.signup_view, name='signup'), # Will create signup_view in accounts/views.py
    path('profile/', views.profile_view, name='profile'), # Will create profile_view in accounts/views.py
]