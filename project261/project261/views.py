"""
File:       project261/project261/views.py
Language:   Python 3 with Django Web Framework

Author:     Val Booth <vxb4825@rit.edu>
Author:     Corban Mailloux <cdm3806@rit.edu>
Author:     Adam McCarthy <aem1269@rit.edu>
Author:     Michael Washburn <mdw7326@rit.edu>
Author:     Bryon Wilkins <brw4824@rit.edu>

All of the different views or types of pages we need for this toolshare project.
"""

from django.contrib import auth
from django.contrib.auth import views
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from toolshare.forms import *
from toolshare.models import *
from toolshare.utils import *


def register(request):
    """
    A view for the registration.
    This will send the user to the registration form where it will
    require them to fill out user and address information. Then it will
    automatically log them in granted it was a valid form.
    """
    hidesharezone = 'sharezone' in request.session
    sharezone_selection_form = None
    if hidesharezone:
        if request.method == "POST":
            user_form = UserForm(request.POST)
            address_form = AddressForm(request.POST)
            if address_form.is_valid() and user_form.is_valid():
                address = address_form.save()
                user = user_form.save()
                # next two lines actually creates the user
                # When a user comes from creating a sharezone, set it, and default the user to be an admin, and be un-approved.
                new_profile = UserProfile(user=user, address=address, sharezone=request.session.get('sharezone'), is_sharezone_admin=True, is_approved=False)
                new_profile.save()
                request.session.pop('sharezone', None)
                #Next two lines automatically log the user in
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth.logout(request)
                auth.login(request, user)
                return HttpResponseRedirect(reverse('toolshare:user_profile', args = [str(user.id)]))
        else:
            address_form = AddressForm()
            user_form = UserForm()
    else: # This user is not coming from the "Create a Sharezone" page.
        if request.method == "POST":
            user_form = UserForm(request.POST)
            address_form = AddressForm(request.POST)
            sharezone_selection_form = SharezoneSelectionForm(request.POST)
            if address_form.is_valid() and user_form.is_valid() and sharezone_selection_form.is_valid():
                address = address_form.save()
                user = user_form.save()
                sharezone = sharezone_selection_form.save(commit=False).sharezone

                # Next two lines actually creates the user
                new_profile = UserProfile(user=user, address=address, sharezone=sharezone)
                new_profile.save()

                # Send message to all sharezone admins to approve this user.
                sendUserNeedsApprovalMessage(user)

                # Next two lines automatically log the user in
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth.logout(request)
                auth.login(request, user)
                return HttpResponseRedirect(reverse('toolshare:user_profile', args = [str(user.id)]))
        else:
            address_form = AddressForm()
            sharezone_selection_form = SharezoneSelectionForm()
            user_form = UserForm()
    forms = [user_form, sharezone_selection_form, address_form]
    context = {
        'forms'     : forms,
        'hidesharezone'  : hidesharezone
    }
    return render(request, "registration/register.html", context)


def login(request):
    """
    This function authenticates the users login credentials and attempts to log them
    in.
    """
    if (not request.user.is_authenticated()):
        return views.login(request)
    else:
        return HttpResponseRedirect(reverse('toolshare:user_profile_mine'))


def logout(request):
    """
    This function will attempt to logout. If no user is logged in, then it does
    not error out.
    """
    auth.logout(request)
    return render(request,"registration/logout.html")
