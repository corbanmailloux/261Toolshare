"""
File:       toolshare/actions.py
Language:   Python 3 with Django Web Framework

Author:     Val Booth <vxb4825@rit.edu>
Author:     Corban Mailloux <cdm3806@rit.edu>
Author:     Adam McCarthy <aem1269@rit.edu>
Author:     Michael Washburn <mdw7326@rit.edu>
Author:     Bryon Wilkins <brw4824@rit.edu>

actions.py file for the Toolshare app. Handles actions. See "views.py" for pages/forms.
"""

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from toolshare.models import *
from toolshare.utils import *


########
# TOOL #
########

@login_required
@user_is_approved
def returnTool(request, tool_id):
    """
    Returns the borrowed tool if borrowed. If not it will raise a 404 error.
    """  
    tool = get_object_or_404(Tool, pk=tool_id)
    if (not (tool.administrated_by(request.user) or tool.renter == request.user)):
        raise Http404
    reslist = Reservation.get_current(tool=tool)
    if reslist.count() != 0:
        reservation = reslist[0]
        reservation.end_date = timezone.now()
        reservation.save()
        tool.renter = None
        tool.save()

    if (tool.quality == 1):
        tool.shared = False
        sendRentedRemovedToolMessages(tool)
        sendOwnedRemovedToolMessages(tool)
        tool.delete_future_reservations()
        tool.save()

    return HttpResponseRedirect(reverse('toolshare:tool_info', args = [str(tool_id)]))
    
    
@login_required
@user_is_approved
def removeTool(request, tool_id):
    """
    Removes the tool by setting the is_active flag to False. Notifies appropriate parties
    of tool removal.
    """  
    t = get_object_or_404(Tool, pk=tool_id)
    if (not t.administrated_by(request.user)):
        raise Http404
    sendRentedPermanentlyRemovedTool(t)
    sendOwnedPermanentlyRemovedTool(t)
    t.is_active = False
    t.delete_future_reservations()
    t.save()
    return HttpResponseRedirect(reverse('toolshare:tool_list'))


########
# USER #
########

@login_required
@user_is_approved
def banUser(request, user_id):
    """
    Bans a user
    """
    user = get_object_or_404(User, pk=user_id)
    if not (request.user.profile.is_admin(user.profile.sharezone)):
        raise Http404
    # Raise the ban hammer

    # Use the power of the law to bring the ban hammer down with tremendous 
    # force. Observe in awe as the sheer power of the ban hammer causes all 
    # remnants of the user to disappear before your very eyes. You have won.
    # Justice has triumphed over evil yet again. It's almost over. In just a
    # few short moments, punishment will have been dealt...
    user.profile.ban() 
    # The user is banned.
    # You can go home. Everything is over now.
    return HttpResponseRedirect(reverse('toolshare:admin'))


@login_required
@user_is_approved
def unbanUser(request, user_id):
    """
    Unbans a user
    """
    user = get_object_or_404(User, pk=user_id)
    if not (request.user.profile.is_admin(user.profile.sharezone)):
        raise Http404
    # Raise the unban hammer

    # Use the power of the legal system to bring the unban hammer down with tremendous 
    # force. Observe in awe as the sheer power of the unban hammer causes all 
    # remnants of the user to reappear before your very eyes. You have lost.
    # Evil has triumphed over justice yet again. It's almost over. In just a
    # few short moments, punishment will have been removed...
    user.profile.unban() 
    # The user is unbanned.
    # You can go home. Everything is over now.
    return HttpResponseRedirect(reverse('toolshare:admin'))


@login_required
@user_is_approved
def approveUser(request, user_id):
    """
    Approves a user
    """
    user = get_object_or_404(User, pk=user_id)

    if not (request.user.profile.is_admin(user.profile.sharezone)):
        raise Http404

    # Approve the user
    user.profile.approve()

    return HttpResponseRedirect(reverse('toolshare:admin'))


@login_required
@user_is_approved
def makeSharezoneAdmin(request, user_id):
    """
    Makes a user into a sharezone admin
    """
    user = get_object_or_404(User, pk=user_id)

    if not (request.user.profile.is_admin(user.profile.sharezone)):
        raise Http404

    # Approve the user
    user.profile.make_sharezone_admin()

    return HttpResponseRedirect(reverse('toolshare:admin'))


@login_required
@user_is_approved
def removeSharezoneAdmin(request, user_id):
    """
    Makes a sharezone admin into a regular user
    """
    user = get_object_or_404(User, pk=user_id)

    if not (request.user.profile.is_admin(user.profile.sharezone)):
        raise Http404

    # Approve the user
    user.profile.remove_sharezone_admin()

    return HttpResponseRedirect(reverse('toolshare:admin'))


#############
# SHAREZONE #
#############

# No longer in use.
# @login_required
# @user_is_approved
# def removeSharezone(request, sharezone_id):
#     """
#     Removes (inactivates) a sharezone.
#     """
#     sharezone = get_object_or_404(Sharezone, pk=sharezone_id)

#     if (not (request.user.is_superuser or (request.user.is_sharezone_admin and
#         request.user.profile.sharezone == sharezone))):
#         raise Http404

#     # Remove the sharezone
#     sharezone.remove()

#     return HttpResponseRedirect(reverse('toolshare:admin'))


@login_required
@user_is_approved
@user_passes_test(lambda u: u.profile.is_admin()) # If the users isn't a superuser, it redirects them to their profile
def approveSharezone(request, sharezone_id):
    """
    Approves a sharezone, and also approve the sharezone admins
    """
    sharezone = get_object_or_404(Sharezone, pk=sharezone_id)

    # Approve the sharezone
    sharezone.approve()

    # Approve each sharezone admin. This actually gets all users, but the only user will be the admin.
    for sharezone_admin in list(sharezone.get_user_list(approved=False)):
        sharezone_admin.profile.approve()

    return HttpResponseRedirect(reverse('toolshare:admin'))
