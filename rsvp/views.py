# rsvp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages # Import the messages framework
from .models import RSVP, Guest
from .forms import RSVPForm, GuestFormSet, GuestForm
from django.forms import inlineformset_factory

# rsvp/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RSVPForm, GuestForm
from .models import RSVP, Guest
from django.forms import inlineformset_factory

def rsvp_submission_view(request):
    rsvp_instance = None
    # If user is authenticated, try to get their existing RSVP
    if request.user.is_authenticated:
        try:
            rsvp_instance = RSVP.objects.get(user=request.user)
        except RSVP.DoesNotExist:
            pass  # No existing RSVP, so rsvp_instance remains None

    # Dynamically set extra forms based on whether guests exist
    extra_forms = 0 if rsvp_instance and rsvp_instance.guests.exists() else 2

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
        # Pass instance if it exists, for both logged-in and anonymous users
        rsvp_form = RSVPForm(request.POST, instance=rsvp_instance)
        guest_formset = GuestFormSetDynamic(request.POST, instance=rsvp_instance, prefix='guests')

        if rsvp_form.is_valid() and guest_formset.is_valid():
            rsvp = rsvp_form.save(commit=False)
            if request.user.is_authenticated:
                rsvp.user = request.user
            
            # If the user is not logged in, we must ensure the email is unique
            # or retrieve the existing RSVP associated with that email.
            if not request.user.is_authenticated:
                email = rsvp_form.cleaned_data.get('email')
                existing_rsvp = RSVP.objects.filter(email=email, user__isnull=True).first()
                if existing_rsvp:
                    rsvp.pk = existing_rsvp.pk # Update existing RSVP
                    rsvp.id = existing_rsvp.id

            rsvp.save() # Save the RSVP instance to get a PK for the formset

            # Re-bind the formset to the now-saved RSVP instance
            guest_formset = GuestFormSetDynamic(request.POST, instance=rsvp, prefix='guests')
            if guest_formset.is_valid(): # Re-validate
                guest_formset.save()
                rsvp.number_of_guests = rsvp.guests.count()
                rsvp.save()

                messages.success(request, 'Your RSVP has been submitted successfully! Thank you.')
                return redirect('rsvp_success')
            else:
                # This case handles errors in the guest formset after the main form is processed
                messages.error(request, 'Please correct the errors in the guest details.')

        else:
            # If forms are not valid, add an error message and re-render with errors
            messages.error(request, 'Please correct the errors below.')
    else:
        # GET request: Display empty forms or pre-populate if RSVP exists
        initial_data = {}
        if request.user.is_authenticated and not rsvp_instance:
            initial_data['email'] = request.user.email

        rsvp_form = RSVPForm(instance=rsvp_instance, initial=initial_data)
        guest_formset = GuestFormSetDynamic(instance=rsvp_instance, prefix='guests')

    context = {
        'rsvp_form': rsvp_form,
        'guest_formset': guest_formset,
    }
    return render(request, 'rsvp/rsvp_form.html', context)

# simple view success page
def rsvp_success_view(request):
    return render(request, 'rsvp/rsvp_success.html')