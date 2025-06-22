# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserProfileForm
from .models import CustomUser
from rsvp.models import RSVP, Guest

def signup_view(request):
    """
    Handles user registration.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login') # Redirect to the login page after successful registration
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile_view(request):
    """
    Displays the user's profile and allows them to update their details.
    Also displays their associated RSVP status.
    """
    user = request.user # Get the logged-in user instance

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile') # Redirect back to the profile page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=user) # Pre-populate form with existing user data

    # --- CORRECTED RSVP Lookup Logic ---
    user_rsvp = None
    guests_in_party = []
    try:
        # Get the RSVP submission directly linked to the current user
        user_rsvp = RSVP.objects.get(user=user)
        # If an RSVP exists, get all guests associated with that specific RSVP
        # 'guests' is the related_name defined in your Guest model's ForeignKey to RSVP
        guests_in_party = user_rsvp.guests.all()
    except RSVP.DoesNotExist:
        # No RSVP found for this user
        user_rsvp = None
        guests_in_party = [] # Ensure this is an empty list if no RSVP
    # --- End CORRECTED RSVP Lookup Logic ---

    context = {
        'form': form,
        'user_rsvp': user_rsvp,         # Pass the RSVP object itself (will be None if not found)
        'guests_in_party': guests_in_party # Pass the list of guests (can be empty)
    }
    return render(request, 'accounts/profile.html', context)