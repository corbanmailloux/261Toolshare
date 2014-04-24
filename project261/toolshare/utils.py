"""
File:       project261/toolshare/utils.py
Language:   Python 3 with Django Web Framework

Author:     Val Booth <vxb4825@rit.edu>
Author:     Corban Mailloux <cdm3806@rit.edu>
Author:     Adam McCarthy <aem1269@rit.edu>
Author:     Michael Washburn <mdw7326@rit.edu>
Author:     Bryon Wilkins <brw4824@rit.edu>

Helper functions used in toolshare that have nowhere else to go.
"""

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import available_attrs
from functools import wraps
from toolshare.models import *
from postman.api import *


def getSystemUser():
    """
    Use get_or_create to get (or create) the SYSTEM user.
    """
    return User.objects.get_or_create(username="SYSTEM", defaults={
        'first_name'    : "SYS",
        'last_name'     : "TEM",
        'password'      : "This_is_a_password",
        'email'         : "toolshare@corb.co"
        })[0]


def sendRentedRemovedToolMessages(tool):
    """
    params: tool, a tool object
    
    A function to send people with reservations on a removed tool a
    notification that the tool has been removed.
    """
    reservations = list(tool.get_future_reservations())
    sender = getSystemUser()
    
    for reservation in reservations:
        recipient = reservation.user
        subject = tool.name + " Has Been Removed"

        body = """Dear %s,
        A tool you have reserved in the future, \"%s\", has been removed from the system due to a broken quality rating, and your reservation has been deleted.
        The tool will remain inactive unless reinstated into the system by its owner, %s. 

        We apologize for the inconvenience,
        SYSTEM

        Please do not reply to this message.""" % (reservation.user.first_name, tool.name, tool.owner.username)

        pm_write(sender, recipient, subject, body, skip_notification=False,
        auto_archive=False, auto_delete=False, auto_moderators=None)


def sendOwnedRemovedToolMessages(tool):
    """
    params: tool, a tool object
    
    A function to send the owner of a tool a notification in order to alert
    them that their tool is inactive and they should go fix it or remove it.
    """
    sender = getSystemUser()
    recipient = tool.owner
    subject = tool.name + " Has Been Removed"

    body = """Dear %s,
    One of the the tools you own, \"%s\", has been removed from the system due to a broken quality rating. 
    You may:
    1. Retrieve the tool from the sharezone, fix it, and change its quality on its "Edit Tool Info" page to reinstate it into the system.
    2. Use its "Edit Tool Info" page to remove the tool from the sytem entirely.

    Thank you for your consideration,
    SYSTEM

    Please do not reply to this message.""" % (tool.owner.first_name, tool.name)

    pm_write(sender, recipient, subject, body)


def sendOwnedPermanentlyRemovedTool(tool):
    """
    params: tool, a tool object
    
    A function to send the owner of a tool a notification in order to alert
    them that their tool is PERMANENTLY removed. ONLY CALLED IF THE ADMIN DELETES IT.
    """
    sender = getSystemUser()
    recipient = tool.owner
    subject = tool.name + " Has Been Removed"

    body = """Dear %s,
    One of the the tools you own, \"%s\", has been permanently removed from the system by either a sharezone or system admin.
    Please direct any comments, questions or concerns to the above parties.

    Thank you for your consideration,
    SYSTEM

    Please do not reply to this message.""" % (tool.owner.first_name, tool.name)

    pm_write(sender, recipient, subject, body)

def sendRentedPermanentlyRemovedTool(tool):
    """
    params: tool, a tool object
    
    A function to send people with reservations on a removed tool a
    notification that the tool has been permanently removed. That is, the owner deleted it
    from the system.
    """
    reservations = list(tool.get_future_reservations())
    sender = getSystemUser()
    
    for reservation in reservations:
        recipient = reservation.user
        subject = tool.name + " Has Been Removed"

        body = """Dear %s,
        A tool you have reserved in the future, \"%s\", has been permanently removed from the system and your reservation has been deleted.
        

        We apologize for the inconvenience,
        SYSTEM

        Please do not reply to this message.""" % (reservation.user.first_name, tool.name)

        pm_write(sender, recipient, subject, body, skip_notification=False,
        auto_archive=False, auto_delete=False, auto_moderators=None)

def sendUserNeedsApprovalMessage(user):
        """
        params: user, a user object who's trying to join a sharezone
        
        A function to send a sharezone admin a notification that someone wants to join their sharezone
        """
        sender = getSystemUser()
        subject = user.username + " Would Like to Join Your Sharezone"
        recipients = list(user.profile.sharezone.get_admins())
        #This message is purposefully wordy because I want it to be
        for recipient in recipients:
            body = """Dear %s,
            User %s wishes to join your sharezone. Should you wish to approve them, please click the appropriate "Approve User" button in the Users section of your Admin Panel page.

            Thank you for your consideration,
            SYSTEM

            Please do not reply to this message.""" % (recipient.first_name, user.username)
            pm_write(sender, recipient, subject, body)


def sendSharezoneNeedsApprovalMessage(sharezone):
    """
    params: sharezone, a sharezone object so they know what sharezone wants to be approved
    
    A function to send the super admin a message that someone wants to create a sharezone
    """
    superDuperAdmins = list(User.objects.filter(is_superuser=True))
    sender = getSystemUser()
    subject = "New Sharezone Application"
    for superAdmin in superDuperAdmins:
        body = """Dear %s,
        The \"%s\" sharezone is awaiting your approval to join the toolshare system.
        Should you wish to approve this sharezone, please click the appropriate "Approve Sharezone" button in the Sharezones section of your Admin Panel page.

        Thank you for your consideration,
        SYSTEM

        Please do not reply to this message.""" % (superAdmin.first_name, sharezone.name)
        pm_write(sender, superAdmin, subject, body)
    

def sendReservationEndingMessage(reservation):
    """
    params: reservation
    
    A function to send notify a user that their reservation is ending soon.
    """
    sender = getSystemUser()
    recipient = reservation.user
    tool = reservation.tool
    subject = tool.name + "'s Reservation Is Ending Soon"

    body = """Dear %s,
    Your reservation on \"%s\" is ending soon. Please return the the tool prior to its reservation end time, or make another reservation after your current reservation's end time (if available).

    Thank you for your consideration,
    SYSTEM

    Please do not reply to this message.""" % (reservation.user.first_name, tool.name)

    pm_write(sender, recipient, subject, body)


#####################
# Custom Decorators #
#####################

def user_is_approved(view_func, not_approved='toolshare:not_approved'):
    """
    Decorator to test if a user is approved.
    If they aren't, redirect them to the 'Not Approved' page.

    Usage:
        @user_is_approved
        def myView(request):
            ...
    """
    @wraps(view_func, assigned=available_attrs(view_func))
    def wrapper(request, *args, **kwargs):
        if request.user.profile.is_approved:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse(not_approved))
    return wrapper
