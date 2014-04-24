"""
File:       toolshare/views.py
Language:   Python 3 with Django Web Framework

Author:     Val Booth <vxb4825@rit.edu>
Author:     Corban Mailloux <cdm3806@rit.edu>
Author:     Adam McCarthy <aem1269@rit.edu>
Author:     Michael Washburn <mdw7326@rit.edu>
Author:     Bryon Wilkins <brw4824@rit.edu>

Views.py file for the Toolshare app. Handles which webpages should be
displayed and how.
"""

from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from toolshare.forms import *
from toolshare.models import *
from toolshare.utils import *


# Publicly Accessible
def home(request):
    """
    The homepage view. Should show some basic statistics and provide a warm welcome
    to our users.
    """
    user_count = UserProfile.objects.filter(user__is_active=True, is_approved=True).count()
    tool_count = Tool.objects.filter(is_active=True).count()
    rental_count = Reservation.objects.filter(start_date__lte=timezone.now()).count()
    sharezone_count = Sharezone.objects.filter(is_active=True).count()
    most_popular_group = ToolGroup.get_largest_group()
    groups = ToolGroup.objects.all()
    most_popular_sharezones = Sharezone.get_largest_sharezones()
    context = {
        'request'                   : request,
        'user_count'                : user_count, 
        'tool_count'                : tool_count,
        'rental_count'              : rental_count, 
        'most_popular_group'        : most_popular_group,
        'sharezone_count'           : sharezone_count,
        'groups'                    : groups,
        'most_popular_sharezones'   : most_popular_sharezones,
    }
    return render(request, "index.html", context)


#########
# ADMIN #
#########

@login_required
@user_is_approved
def admin(request):
    """
    A page where admins can admin.
    """
    if not (request.user.profile.is_admin(request.user.profile.sharezone)):
        raise Http404
    #generate user list and sharezone list
    user_profiles = []
    sharezones = []
    if request.user.is_superuser:
        sharezones = Sharezone.objects.all().order_by('is_approved','name')
        user_profiles = UserProfile.objects.all().order_by('is_approved','user__username')
    else:
        sharezones = [request.user.profile.sharezone]
        user_profiles = UserProfile.objects.filter(sharezone=request.user.profile.sharezone).order_by('is_approved', 'user__username')

    context = {
        "request"       : request,
        "user_profiles" : user_profiles,
        "sharezones"         : sharezones,
        }
    return render(request, "admin/index.html", context)


@login_required
@user_is_approved
def admin_edit_sharezone(request, sharezone_id):
    """
    This view allows admins to edit everything found in the sharezone_edit view with
    the addition of being able to set the is_approved value.
    """
    sharezone = get_object_or_404(Sharezone, pk=sharezone_id)
    # if you are not a superuser or a sharezone admin for this sharezone you cannot access this
    if not (request.user.profile.is_admin(sharezone)):
        raise Http404
    if request.method == "POST":
        approve_form = AdminApproveSharezoneForm(request.POST)
        sharezone_form = SharezoneForm(request.POST)
        address_form = AddressForm(request.POST)
        if address_form.is_valid() and sharezone_form.is_valid() and (approve_form.is_valid() or not request.user.is_superuser):
            address = address_form.save()
            sharezone_form_result = sharezone_form.save(commit=False)
            sharezone.name = sharezone_form_result.name
            sharezone.description = sharezone_form_result.description
            sharezone.address = address
            if request.user.is_superuser:
                approve_form_result = approve_form.save(commit=False)
                sharezone.is_approved = approve_form_result.is_approved
            sharezone.save()
            return HttpResponseRedirect(reverse('toolshare:admin'))
    else:
        approve_form = AdminApproveSharezoneForm(initial={"is_approved":sharezone.is_approved})
        address_form = AddressForm(initial={'line1':sharezone.address.line1,
            'line2':sharezone.address.line2, 'zip':sharezone.address.zip})
        sharezone_form = SharezoneForm(initial={'name':sharezone.name,
            'description':sharezone.description})
    forms = [approve_form, sharezone_form, address_form]
    context = {
        'request'   : request,
        'forms'     : forms,
        'sharezone'      : sharezone 
    }
    return render(request, "admin/edit_sharezone/index.html", context)


@login_required
@user_is_approved
def admin_edit_user(request, user_id):
    """
    Allows the admin to edit ALL user information.
    This includes all the forms used in EditProfile and adds two additional
    forms which allow the admin to change special attributes like is_approved,
    is_sharezone_admin, is_superuser, and is_active found in UserProfile and User.
    """
    user = get_object_or_404(User, pk=user_id)
    if not (request.user.profile.is_admin(user.profile.sharezone)):
        raise Http404
    if request.method == "POST":
        admin_user_form = AdminUserForm(request.POST, instance=user)
        admin_profile_form = AdminProfileForm(request.POST, instance=user.profile)
        user_form = EditUserForm(request.POST, instance=user)
        sharezone_form = SharezoneSelectionForm(request.POST, instance=user.profile)
        address_form = AddressForm(request.POST, instance=user.profile.address)
        if user_form.is_valid() and address_form.is_valid() and sharezone_form.is_valid():
            user.first_name = user_form.cleaned_data["first_name"]
            address = address_form.save()
            sharezone_form_result = sharezone_form.save(commit=False)
            sharezone = sharezone_form_result.sharezone
            sharezone.save()
            user.profile.sharezone = sharezone
            user.profile.address = address
            #admin stuff
            admin_user_result = admin_user_form.save(commit=False)
            admin_profile_result = admin_profile_form.save(commit=False)
            if request.user.is_superuser:
                user.is_superuser = admin_user_result.is_superuser
            user.is_active = admin_user_result.is_active
            user.profile.is_approved = admin_profile_result.is_approved
            user.profile.is_sharezone_admin = admin_profile_result.is_sharezone_admin
            user.profile.save()
            user.save()
            return HttpResponseRedirect(reverse('toolshare:admin'))
    else:
        user_form = EditUserForm(initial={"email":user.email,"first_name":user.first_name,"last_name":user.last_name})
        sharezone_form = SharezoneSelectionForm(initial={"sharezone":user.profile.sharezone})
        address_form = AddressForm(initial={"line1":user.profile.address.line1,"line2":user.profile.address.line2,"zip":user.profile.address.zip})
        admin_user_form = AdminUserForm(initial={"is_superuser":user.is_superuser,"is_active":user.is_active})
        admin_profile_form = AdminProfileForm(initial={"is_approved":user.profile.is_approved,"is_sharezone_admin":user.profile.is_sharezone_admin})
    forms = [admin_profile_form, admin_user_form, user_form, sharezone_form, address_form]
    context = {
        'request'       : request, 
        'forms'         : forms, 
        'user_editing'  : user,
    }
    return render(request,"admin/edit_user/index.html", context)


#############
# SHAREZONE #
#############

# Publicly Accessible
def sharezone_create(request):
    """
    Creates a new sharezone using a form to get the first and second
    line of the sharezone address, along with other information.
    """
    if request.method == "POST":
        sharezone_form = SharezoneForm(request.POST)
        address_form = AddressForm(request.POST)
        if address_form.is_valid() and sharezone_form.is_valid():
            address = address_form.save()
            sharezone = sharezone_form.save(commit=False)
            sharezone.address = address
            sharezone.save()
            # Send message to all superusers
            sendSharezoneNeedsApprovalMessage(sharezone)
            # Store a cookie...
            request.session['sharezone'] = sharezone
            return HttpResponseRedirect(reverse('register'))
    else:
        auth.logout(request)
        address_form = AddressForm()
        sharezone_form = SharezoneForm()
    forms = [sharezone_form, address_form]
    context = {
        'forms' : forms
    }
    return render(request, "sharezone/register/index.html", context)


@login_required
@user_is_approved
def sharezone(request, sharezone_id=None):
    #sharezone/info
    """
    Displays basic information about a sharezone.
    """
    if (sharezone_id is None):
        sharezone = request.user.profile.sharezone
    elif (request.user.profile.is_admin()):
        sharezone = get_object_or_404(Sharezone, pk=sharezone_id)
    else:
        return HttpResponseRedirect(reverse('toolshare:sharezone'))
    number_of_users = User.objects.filter(profile__sharezone=sharezone).count()
    most_used_tool = sharezone.get_most_used_tool()
    most_active_borrower = sharezone.get_most_active_borrower()
    most_active_lender = sharezone.get_most_active_lender()
    number_of_shares = sharezone.get_number_of_shares()
    most_recent_tool = sharezone.get_most_recent_tool()
    users = sharezone.get_non_admins()
    admins = sharezone.get_admins()
    number_of_users = sharezone.get_user_list().count()

    class Group: # Create a container class
        __slots__ = ("name", "size", "tools")

    groups = []
    for toolGroup in ToolGroup.objects.all():
        group = Group()
        group.name = toolGroup.name
        group.tools = Tool.objects.filter(group=toolGroup, sharezone=sharezone, is_active=True, shared=True).order_by('-quality')
        group.size = group.tools.count()
        groups.append(group)
    
    context = {
        "request"               : request,
        "sharezone"             : sharezone,
        "most_used_tool"        : most_used_tool,
        "most_active_borrower"  : most_active_borrower,
        "most_active_lender"    : most_active_lender,
        "number_of_shares"      : number_of_shares,
        "number_of_users"       : number_of_users,
        "most_recent_tool"      : most_recent_tool,
        "users"                 : users,
        "admins"                : admins,
        "groups"                : groups
    }

    return render(request, "sharezone/index.html", context)

    
@login_required
@user_is_approved
def sharezone_tools(request, sharezone_id=None):
    #sharezone/info
    """
    Displays basic information about a sharezone.
    """
    if (sharezone_id is None):
        sharezone = request.user.profile.sharezone
    elif (request.user.profile.is_admin()):
        sharezone = get_object_or_404(Sharezone, pk=sharezone_id)
    else:
        return HttpResponseRedirect(reverse('toolshare:sharezone_tools'))

    class Group: # Create a container class
        __slots__ = ("name", "size", "tools")

    groups = []
    for toolGroup in ToolGroup.objects.all():
        group = Group()
        group.name = toolGroup.name
        group.tools = Tool.objects.filter(group=toolGroup, sharezone=sharezone, is_active=True, shared=True).order_by('-quality')
        group.size = group.tools.count()
        groups.append(group)
    
    context = {
        "request"               : request,
        "sharezone"             : sharezone,
        "groups"                : groups
    }

    return render(request, "sharezone/tools/index.html", context)


@login_required
@user_is_approved
def sharezone_edit(request):
    """
    This view is used to edit a sharezone. Only Admins of the sharezone
    or the super admin can access it
    """
    if (not (request.user.is_superuser or request.user.profile.is_sharezone_admin)):
        raise Http404
    if request.method == "POST":
        sharezone_form = SharezoneForm(request.POST)
        address_form = AddressForm(request.POST)
        if address_form.is_valid() and sharezone_form.is_valid():
            sharezone = request.user.profile.sharezone
            address = address_form.save()
            sharezone_form_result = sharezone_form.save(commit=False)
            sharezone.name = sharezone_form_result.name
            sharezone.description = sharezone_form_result.description
            sharezone.address = address
            sharezone.save()
            request.user.profile.save()
            sharezone.save()
            return HttpResponseRedirect(reverse('toolshare:sharezone'))
    else:
        address_form = AddressForm(initial={'line1':request.user.profile.sharezone.address.line1,
            'line2':request.user.profile.sharezone.address.line2, 'zip':request.user.profile.sharezone.address.zip})
        sharezone_form = SharezoneForm(initial={'name':request.user.profile.sharezone.name,
            'description':request.user.profile.sharezone.description})
    forms = [sharezone_form, address_form]
    context = {
        'forms' : forms
    }
    return render(request, "sharezone/edit/index.html", context)


########
# TOOL #
########

@login_required
@user_is_approved
@user_passes_test(lambda u: u.profile.is_admin()) # If the users isn't a superuser, it redirects them to their profile
def tool_list(request):
    #/tool/list
    """
    This view will display a list of all tools sorted by ToolGroup
    """
    # I HATE THE FOLLOWING LINE!
    Tool.update_all()
    group_list = ToolGroup.objects.all()
    context = {
        'group_list': group_list
    }
    return render(request, 'tool/index.html', context)


@login_required
@user_is_approved
def tool_register(request):
    #/tool/register
    """
    This view allows the user to register a tool under their own name.
    Users cannot register a tool for someone else.
    """
    forms = []
    if request.method == "POST":
        form = ToolForm(request.POST)
        if form.is_valid():
            
            # commit=False means the form doesn't save at this time.
            # commit defaults to True which means it normally saves.
            tool = form.save(commit=False)

            # Set owner to the currently logged in user.
            tool.owner = request.user
            tool.sharezone = request.user.profile.sharezone

            # Unshare if broken.
            if (int(tool.quality) == 1):
                tool.shared = False

            tool.save()
            # Redirect to tool info page
            return HttpResponseRedirect(reverse('toolshare:tool_info', args = [str(tool.id)]))
    else:
        form = ToolForm(initial={
            'quality' : 3
            })

    forms = [form]
    context = {
        'forms' : forms
    }
    return render(request, "tool/register/index.html", context)


@login_required
# @user_is_approved
# This view requires manual user validation
def tool_info(request, tool_id): 
    #/tool/info/[tool_id]
    """
    Tool info displays all relevant tool information. It allows the user
    to view the tools page and decide whether or not to borrow a tool
    """
    tool = get_object_or_404(Tool, pk=tool_id)
    if not tool.viewable_by(request.user): #Ensure the user can view this page.
        raise Http404
    # I HATE THE FOLLOWING LINE!
    tool.update()
    you_have_tool = (tool.renter == request.user)
    owner_id = tool.owner.id
    can_edit = tool.administrated_by(request.user)
    can_force_return = (tool.renter is not None and can_edit)
    # renter_id CANNOT be guarenteed to be a valid id. Test if == None first.
    renter_id = None
    if (tool.renter is not None):
        renter_id = tool.renter.id
    context = {
        'request'             : request,
        'tool'                : tool, 
        'you_have_tool'       : you_have_tool,
        'owner_id'            : owner_id, 
        'renter_id'           : renter_id, 
        'can_edit'            : can_edit, 
        'can_force_return'    : can_force_return,
        'future_reservations' : tool.get_future_reservations()
    }
    return render(request, 'tool/info/index.html', context)
    

@login_required
@user_is_approved
def tool_edit(request, tool_id):
    #/tool/info/edit/[tool_id]
    """
    Allows a user to change information about a tool. If the user
    trying to access the page doesn't own it they get a 404
    """
    tool = get_object_or_404(Tool, pk=tool_id)
    # I HATE THE FOLLOWING LINE!
    tool.update()
    if (not tool.administrated_by(request.user)):
        raise Http404


    if request.method == "POST":
        form = ToolForm(request.POST, instance=tool)
        if form.is_valid():
            tool.name = form.cleaned_data["name"]
            tool.group = form.cleaned_data["group"]
            tool.quality = form.cleaned_data["quality"]
            tool.shared = form.cleaned_data["shared"]

            # Unshare if broken.
            if (int(tool.quality) == 1):
                tool.shared = False
                sendRentedRemovedToolMessages(tool)
                tool.delete_future_reservations()

            tool.save()
            return HttpResponseRedirect(reverse('toolshare:tool_info', args = [str(tool_id)]))
    else:
        form = ToolForm(initial={
            "name"          :  tool.name,
            "group"         :  tool.group,
            "quality"       :  tool.quality,
            "shared"        :  tool.shared,
            "description"   :  tool.description,
            "instructions"  :  tool.instructions
            })

    #TODO
    #Check if it can be borrowed, mean it's available and you can change the sharedness
    #The opposite of that it true so therefore shared must be hidden

    shared_available = (tool.get_future_reservations().count() == 0)
    context = {
        'form'             : form, 
        'shared_available'  : shared_available
    }
    return render(request,"tool/edit/index.html", context)


@login_required
@user_is_approved
def tool_reserve(request, tool_id):
    #/tool/reserve/[tool_id]
    """
    Allows a user to change information about a tool. If the user
    trying to access the page doesn't own it they get a 404
    """
    tool = get_object_or_404(Tool, pk=tool_id, sharezone=request.user.profile.sharezone)
    tool.update()
    if request.method == "POST":
        reservation_form = ReservationForm(request.POST, instance=tool)
        if reservation_form.is_valid():
            start_date = reservation_form.cleaned_data["start_date"]
            end_date = reservation_form.cleaned_data["end_date"]
            reservation = Reservation(start_date=start_date,end_date=end_date, tool=tool, user= request.user)
            if reservation.is_valid():
                reservation.save()
                return HttpResponseRedirect(reverse('toolshare:tool_info', args = [str(tool_id)]))
    else:
        now = datetime.datetime.now()
        reservation_form = ReservationForm(initial={
            'start_date'    : now.strftime("%m/%d/%Y %I:%M %p"),
            'end_date'      : (now + datetime.timedelta(weeks=2)).strftime("%m/%d/%Y %I:%M %p")
            })
    forms = [reservation_form]
    context = {
        'forms'                 : forms, 
        'future_reservations'   : tool.get_future_reservations()
    }
    return render(request,"tool/reservation/index.html", context)


@login_required
@user_is_approved
def tool_return_quality(request, tool_id):
    #/tool/info/quality/[tool_id]
    """
    Allows a borrower to change quality of a tool.
    Raise 404 if the user isn't the borrower.
    """
    tool = get_object_or_404(Tool, pk=tool_id)
    # I HATE THE FOLLOWING LINE!
    tool.update()
    if (tool.renter != request.user):
        raise Http404

    if request.method == "POST":
        form = EditToolQualityForm(request.POST, instance=tool)
        if form.is_valid():
            tool.quality = form.cleaned_data["quality"]
            tool.save()
            return HttpResponseRedirect(reverse('toolshare:returnTool', args = [str(tool_id)]))
    else:
        form = EditToolQualityForm(initial={
                "quality" : tool.quality
            })

    context = {
        'form' : form
    }
    return render(request, "tool/return/index.html", context)


#############
# TOOLGROUP #
#############

@login_required
@user_is_approved
@user_passes_test(lambda u: u.profile.is_admin()) # If the users isn't a superuser, it redirects them to their profile
def toolgroup(request):
    """
    Allows the creation of a new ToolGroup.
    """
    if request.method == "POST":
        tool_group_form = ToolGroupForm(request.POST)
        if tool_group_form.is_valid():
            tool_group_form.save()
            return HttpResponseRedirect(reverse('toolshare:toolgroup'))
    else:
        tool_group_form = ToolGroupForm()
    forms = [tool_group_form]
    context = {
        'forms'             : forms,
        'toolgroup_list'    : ToolGroup.objects.all()
    }
    return render(request, "toolgroup/index.html", context)


@login_required
@user_is_approved
@user_passes_test(lambda u: u.profile.is_admin()) # If the users isn't a superuser, it redirects them to their profile
def toolgroup_edit(request, toolgroup_id):
    """
    Allows an admin to edit the name of an existing ToolGroup.
    """
    toolgroup = get_object_or_404(ToolGroup, pk=toolgroup_id)

    if request.method == "POST":
        tool_group_form = ToolGroupForm(request.POST, instance=toolgroup)
        if tool_group_form.is_valid():
            tool_group_form.save()
            return HttpResponseRedirect(reverse('toolshare:toolgroup'))
    else:
        tool_group_form = ToolGroupForm(initial={
                'name' : toolgroup.name
            })
    forms = [tool_group_form]
    context = {
        'forms'             : forms
    }
    return render(request, "toolgroup/edit/index.html", context)


########
# USER #
########

@login_required
@user_is_approved
@user_passes_test(lambda u: u.profile.is_admin()) # If the users isn't a superuser, it redirects them to their profile
def user_list(request):
    #/user/list
    """
    This view shows a list of all users
    The template will allow a user to get the user profiles of all users in the system
    """
    context = {
        'userlist' : UserProfile.objects.filter(user__is_active=True)
    }
    return render(request, 'user/list/index.html', context)


@login_required
def user_profile(request, user_id): 
    #users/profile/[user_id]
    """
    This view shows the user all relevant information to their profile.
    The template will also allow the user to edit their profile by directing
    them to EditProfile below.
    """
    profile = get_object_or_404(UserProfile, user__id=user_id) #This can stay
    ownedTools = Tool.objects.filter(owner=profile.user.id, is_active=True
        ).order_by('-name')
    rentedTools = Tool.objects.filter(renter=profile.user.id, is_active=True
        ).order_by('-name')
    context = {
        'request'       : request,
        'profile'       : profile,
        'ownedTools'    : ownedTools,
        'rentedTools'   : rentedTools,
    }
    return render(request, 'user/profile/index.html', context)


@login_required
def user_profile_mine(request):
    """
    Returns the requested user's profile
    """
    return user_profile(request, request.user.id)
    

@login_required
def user_profile_edit(request):
    #users/profile/edit
    """
    Allow a user to change their own personal information.
    """
    user = request.user

    if request.method == "POST":
        user_form = EditUserForm(request.POST, instance=user)
        sharezone_form = SharezoneSelectionForm(request.POST)
        address_form = AddressForm(request.POST, instance=user.profile.address)
        if user_form.is_valid() and address_form.is_valid() and sharezone_form.is_valid():
            # This handles the first_name, last_name, and email.
            user_form.save()
            # This handles the whole address.
            address_form.save()

            # Get the new sharezone.
            new_sharezone = sharezone_form.save(commit=False).sharezone
            # If the user is changing their sharezone, unapprove and unadmin them.
            if (new_sharezone != user.profile.sharezone):
                if not user.is_superuser:
                    user.profile.is_approved = False
                for t in user.ownedtool_set.all():
                    #Delete all the user's tools
                    t.is_active = False
                    sendRentedPermanentlyRemovedTool(t)
                    sendOwnedPermanentlyRemovedTool(t)
                    t.delete_future_reservations()
                    t.save()

                user.profile.is_sharezone_admin = False
                # Change the user's sharezone and save the user.
                user.profile.sharezone = new_sharezone
                user.profile.save()
                # Send message to all sharezone admins to approve this user.
                sendUserNeedsApprovalMessage(user)
            user.profile.save() # Don't know if this is necessary.

            return HttpResponseRedirect(reverse('toolshare:user_profile', args = [str(request.user.id)]))
    else:
        user_form = EditUserForm( initial = {
            'first_name'  :  request.user.first_name,
            'last_name'   :  request.user.last_name,
            'email'       :  request.user.email,
            })
        sharezone_form = SharezoneSelectionForm( initial = {
            'sharezone'        :  request.user.profile.sharezone,
            })
        address_form = AddressForm( initial = {
            'line1'       :  request.user.profile.address.line1,
            'line2'       :  request.user.profile.address.line2,
            'zip'         :  request.user.profile.address.zip,
            })
    
    forms = [user_form, sharezone_form, address_form]
    context = {
        'request'   : request,
        'forms'     : forms
    }
    return render(request,"user/profile/edit/index.html", context)


#########
# OTHER #
#########

def not_approved(request):
    context = {
        'request' : request,
    }
    return render(request, '401.html', context)
