# rsvp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages # Import the messages framework
from .models import RSVP, Guest
from .forms import RSVPForm, GuestFormSet # Import forms

@login_required
def rsvp_submission_view(request):
    # Try to get the existing RSVP for the logged-in user
    # If it doesn't exist, RSVP_instance will be None initially for GET requests
    # and will be created on POST
    rsvp_instance = None
    try:
        rsvp_instance = RSVP.objects.get(user=request.user)
    except RSVP.DoesNotExist:
        pass # No existing RSVP, so rsvp_instance remains None

    if request.method == 'POST':
        # Instantiate the main RSVP form with POST data
        rsvp_form = RSVPForm(request.POST, instance=rsvp_instance)
        # Instantiate the Guest formset. If rsvp_instance exists, link it.
        guest_formset = GuestFormSet(request.POST, request.FILES, instance=rsvp_instance, prefix='guests')

        if rsvp_form.is_valid() and guest_formset.is_valid():
            # Save the RSVP instance first
            current_rsvp = rsvp_form.save(commit=False)
            current_rsvp.user = request.user # Link RSVP to the logged-in user
            current_rsvp.save()

            # Save the Guest formset
            # This handles creating new guests, updating existing ones, and deleting marked ones.
            guest_formset.instance = current_rsvp # Link the formset to the just-saved RSVP
            guest_formset.save()

            messages.success(request, 'Your RSVP has been submitted successfully! Thank you.')
            return redirect('rsvp_success') # Redirect to a success URL

        else:
            # If forms are not valid, add an error message and re-render with errors
            messages.error(request, 'Please correct the errors below.')
    else:
        # GET request: Display empty forms or pre-populate if RSVP exists
        rsvp_form = RSVPForm(instance=rsvp_instance)
        guest_formset = GuestFormSet(instance=rsvp_instance, prefix='guests') # Ensure prefix is consistent

    context = {
        'rsvp_form': rsvp_form,
        'guest_formset': guest_formset,
    }
    return render(request, 'rsvp/rsvp_form.html', context)

# simple view success page
def rsvp_success_view(request):
    return render(request, 'rsvp/rsvp_success.html')