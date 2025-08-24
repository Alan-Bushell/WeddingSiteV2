# rsvp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages # Import the messages framework
from .models import RSVP, Guest
from .forms import RSVPForm, GuestFormSet, GuestForm
from django.forms import inlineformset_factory

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

    # Dynamically set extra
    if rsvp_instance and rsvp_instance.guests.exists():
        extra_forms = 0
    else:
        extra_forms = 2

    GuestFormSetDynamic = inlineformset_factory(
        RSVP,
        Guest,
        form=GuestForm,
        can_delete=True,
        extra=extra_forms,
        max_num=10,
        min_num=0,
        validate_min=False
    )

    if request.method == 'POST':
        rsvp_form = RSVPForm(request.POST, instance=rsvp_instance)
        guest_formset = GuestFormSetDynamic(request.POST, instance=rsvp_instance, prefix='guests')
        if rsvp_form.is_valid() and guest_formset.is_valid():
            rsvp = rsvp_form.save()
            guest_formset.save()
            rsvp.number_of_guests = rsvp.guests.count()
            rsvp.save()

            messages.success(request, 'Your RSVP has been submitted successfully! Thank you.')
            return redirect('rsvp_success') # Redirect to a success URL

        else:
            # If forms are not valid, add an error message and re-render with errors
            messages.error(request, 'Please correct the errors below.')
    else:
        # GET request: Display empty forms or pre-populate if RSVP exists
        rsvp_form = RSVPForm(instance=rsvp_instance)
        guest_formset = GuestFormSetDynamic(instance=rsvp_instance, prefix='guests') # Ensure prefix is consistent

    context = {
        'rsvp_form': rsvp_form,
        'guest_formset': guest_formset,
    }
    return render(request, 'rsvp/rsvp_form.html', context)

# simple view success page
def rsvp_success_view(request):
    return render(request, 'rsvp/rsvp_success.html')