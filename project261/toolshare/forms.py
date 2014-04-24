"""
File:       project261/toolshare/forms.py
Language:   Python 3 with Django Web Framework

Author:     Val Booth <vxb4825@rit.edu>
Author:     Corban Mailloux <cdm3806@rit.edu>
Author:     Adam McCarthy <aem1269@rit.edu>
Author:     Michael Washburn <mdw7326@rit.edu>
Author:     Bryon Wilkins <brw4824@rit.edu>

All of the types of forms in use by the toolshare app.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *


#########
# ADMIN #
#########

class AdminApproveSharezoneForm(ModelForm):
    """
    Allows the admin to approve and un-approve sharezones.
    """
    is_approved = forms.BooleanField(label="Approved",required=False)

    class Meta:
        model = Sharezone
        fields = ["is_approved"]


class AdminUserForm(ModelForm):
    """
    Allows an admin to ban a user.
    """
    is_superuser = forms.BooleanField(label="Is Superuser",required=False)
    is_active = forms.BooleanField(label="Is Active",required=False)

    class Meta:
        model = User
        fields = ["is_active", "is_superuser"]


class AdminProfileForm(ModelForm):
    """
    Allows an admin to approve user_profiles for sharezones.
    """
    is_approved = forms.BooleanField(label="Approved",required=False)
    is_sharezone_admin = forms.BooleanField(label="Sharezone Admin",required=False)

    class Meta:
        model = UserProfile
        fields = ["is_approved", "is_sharezone_admin"]


########
# TOOL #
########

class ToolForm(ModelForm):
    """
    Allows the user to create and edit their tool information. 
    """
    choices = [(5, '★★★★★ - Perfect'), (4, '★★★★☆ - Good'), (3, '★★★☆☆ - Average'), (2, '★★☆☆☆ - Poor'), (1, '★☆☆☆☆ - Broken')]
    quality = forms.ChoiceField(choices=choices)

    def __init__(self, *args, **kwargs):
        super(ToolForm, self).__init__(*args,**kwargs)
    
    class Meta:
        model = Tool
        fields = ['name', 'group', 'quality', 'shared', 'description', 'instructions']


class EditToolQualityForm(ModelForm):
    """
    Allows a borrower to edit a returning tool's quality. 
    """
    choices = [(1, '★☆☆☆☆ - Broken'), (2, '★★☆☆☆ - Poor'), (3, '★★★☆☆ - Average'), (4, '★★★★☆ - Good'), (5, '★★★★★ - Perfect')]
    quality = forms.ChoiceField(choices=choices)

    def __init__(self, *args, **kwargs):
        super(EditToolQualityForm, self).__init__(*args,**kwargs)
    
    class Meta:
        model = Tool
        fields = ["quality"]


class ReservationForm(ModelForm):
    """
    Allows a user to create a tool reservation.
    A reservation:
        - can start either immediately or some point in the future
        - has a maximum duration of 2 weeks.
    """

    start_date = forms.DateTimeField(label='Start Date', input_formats=[
        "%m/%d/%Y %I:%M %p", 
        "%m/%d/%y %I:%M %p", 
        "%m/%d/%y %I:%M:%S %p", 
        "%m/%d/%Y %I:%M:%S %p"
        ])
    end_date = forms.DateTimeField(label='End Date', input_formats=[
        "%m/%d/%Y %I:%M %p", 
        "%m/%d/%y %I:%M %p", 
        "%m/%d/%y %I:%M:%S %p", 
        "%m/%d/%Y %I:%M:%S %p"
        ])

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args,**kwargs)
    
    class Meta:
        model = Reservation
        fields = ['start_date', 'end_date']

    def clean(self):
        """
        Internal method to clean the reservation.
        Errors:
            - reservation length is greater than 2 weeks
            - reservation conflicts with an existing reservation
            - start_date is more than an hour in the past
        """
        cleaned_data = super(ReservationForm, self).clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            testReservation = Reservation(start_date=start_date, end_date=end_date, tool=self.instance)
            delStart = False
            delEnd = False

            if (not testReservation.is_valid_length()):
                msg = "Reservation length must be between 0 and 2 weeks."
                self._errors["end_date"] = self.error_class([msg])
                delEnd = True

            if (not testReservation.is_not_conflicting()):
                msg = "This reservation conflicts with an existing reservation. See below."
                self._errors["start_date"] = self.error_class([msg])
                delStart = True
            
            if (testReservation.is_too_old()):
                msg = "This reservation is more than an hour in the past. Please update."
                self._errors["start_date"] = self.error_class([msg])
                delStart = True

            # Remove the invalid items from the cleaned data.
            if delStart:
                del cleaned_data["start_date"]

            if delEnd:
                del cleaned_data["end_date"]

        # Always return the full collection of cleaned data.
        return cleaned_data


#############
# TOOLGROUP #
#############

class ToolGroupForm(ModelForm):
    """
    Allows the creation of ToolGroups.
    """
    name = forms.CharField(required=True, label="Name")

    def __init__(self, *args, **kwargs):
        super(ToolGroupForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ToolGroup
        fields = ['name']

    def clean(self):
        """
        Makes sure that ToolGroups with the same name aren't created.
        """
        cleaned_data = super(ToolGroupForm, self).clean()
        name = cleaned_data.get('name')
        delName = False

        if name:
            if ToolGroup.objects.filter(name=name):
                msg = "Sorry, that ToolGroup already exists."
                self._errors['name'] = self.error_class([msg])
                delName = True
            if delName:
                del cleaned_data['name']
        return cleaned_data


########
# USER #
########

class UserForm(UserCreationForm):
    """
    Allows the creation of a new user, with fields:
        - username
        - first_name
        - last_name
        - email
        - password1
        - password2
    """
    #All fields are required
    email = forms.EmailField(label='Email', required=True)
    first_name = forms.CharField(label='First Name', required=True)
    last_name = forms.CharField(label='Last Name', required=True)
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]


class EditUserForm(ModelForm):
    """
    Allows a user to edit their user information. 
    Does not allow a user to change their username or password.
    """
    email = forms.EmailField(label='Email', required=True)
    first_name = forms.CharField(label='First Name', required=True)
    last_name = forms.CharField(label='Last Name', required=True)
    
    def __init__(self, *args, **kwargs):
        """
        Initialize function for EditUserForm
        Accepts UserForm, arguments, any regex for the arguments
        """
        super(EditUserForm,self).__init__(*args,**kwargs)
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


#############
# SHAREZONE #
#############

class SharezoneForm(ModelForm):
    """
    Allows the creation of a new Sharezone.
    """
    name = forms.CharField(required=True, label="Name")
    description = forms.CharField(required=False, label="Description")

    def __init__(self, *args, **kwargs):
        super(SharezoneForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Sharezone
        fields = ['name', 'description']


class SharezoneSelectionForm(ModelForm):
    """
    Allows the selection of an existing Sharezone.
    Used when registering new users or editing profiles.
    """
    sharezone = forms.ModelChoiceField(queryset=Sharezone.objects.filter(is_approved=True, is_active=True), label='Sharezone', required=True)

    class Meta:
        model = UserProfile
        fields = ["sharezone"]


###########
# ADDRESS #
###########

class AddressForm(ModelForm):
    """
    Allows an Address to be created or modified.
    Used for both Sharezones and UserProfiles.
    All fields are required except for line2.
    """
    line1 = forms.CharField(required=True, label="Address Line 1")
    line2 = forms.CharField(required=False, label="Address Line 2")
    zip = forms.CharField(required=True, max_length=5, label="ZIP Code")


    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Address
        fields = ['line1','line2','zip']

    def clean_zip(self):
        """
        Checks to make sure that the zip code being submitted is acceptable
        """
        zip = self.cleaned_data['zip']
        if (Address.zip_is_integer(zip) and len(zip) == 5):
            return zip
        raise forms.ValidationError("Invalid ZIP Code. Please enter five numbers.")
