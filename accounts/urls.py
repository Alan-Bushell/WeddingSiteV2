# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views # Import Django's built-in auth views
from . import views # Import your custom views from accounts/views.py

urlpatterns = [
    # Django's built-in authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'), # Redirects to login page after logout

    # Password Change URLs (for logged-in users)
    # These views handle the logic, you just need to provide the templates.
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),

    # Password Reset URLs (for users who forgot their password)
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    # Your custom account-related URLs
    path('signup/', views.signup_view, name='signup'), # Your custom signup view
    path('profile/', views.profile_view, name='profile'), # Your custom profile view
]