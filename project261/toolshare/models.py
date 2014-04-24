"""
File:       models.py
Language:   Python 3 with Django Web Framework

Author:     Val Booth <vxb4825@rit.edu>
Author:     Corban Mailloux <cdm3806@rit.edu>
Author:     Adam McCarthy <aem1269@rit.edu>
Author:     Michael Washburn <mdw7326@rit.edu>
Author:     Bryon Wilkins <brw4824@rit.edu>

The Django models.py file. Defines classes that will represent data stored in
the database. Anything in the "toolshare" app that needs to be stored should be
represented in here.
"""

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import models
from django.utils import timezone
import datetime
from toolshare.utils import *


class Address(models.Model):
    """
    Holds an address, which can be had by either a user or a sharezone.
    """
    line1 = models.CharField('Address line 1', max_length=200)
    line2 = models.CharField('Address line 2', max_length=200, blank=True)
    zip = models.CharField('ZIP Code', default="00000", max_length=5)

    class Meta:
        verbose_name_plural = "Addresses" # Fixes plural form
    
    def __str__(self):
        """String representation, only really used for administration"""
        return "%s\n%s\n%s" % (self.line1, self.line2, self.zip)

    def __eq__(self, other):
        """Overrides the == function"""
        if not isinstance(other, Address):
            return False
        return (self.line1 == other.line1 and
            self.line2 == other.line2 and
            self.zip == other.zip)

    #Static Method
    def zip_is_integer(zip):
        """
        Checks if the zip code is a string that represents a positive integer. Returns
        false otherwise.
        """
        try: # If ZIP is not a valid integer, catch that.
            zip = int(zip)
        except ValueError:
            return False
        return zip >= 0 # Valid ZIP Code


class Sharezone(models.Model):
    """
    Represents a sharezone object

    name = String
    address = Address
    description = String
    is_approved = Boolean
    is_active = Boolean
    """
    name = models.CharField(max_length=200)
    address = models.ForeignKey(Address)
    description = models.CharField(blank=True, max_length=200)
    is_approved = models.BooleanField("Approved?", default=False)
    is_active = models.BooleanField("Active?", default=True)

    def __str__(self):
        """
        returns a string representation of a sharezone
        """
        return self.name

    def get_user_list(self, approved=True):
        """
        Gets a queryset of all active users associated with this sharezone.
        If approved=True, return only members that have been approved.
        If approved=False, return all members that are active.
        """
        if approved: # We only want users that have been approved
            return User.objects.filter(
                profile__sharezone=self,
                is_active=True,
                profile__is_approved=True
                )
        # Otherwise we don't care if they're approved
        return User.objects.filter(
            profile__sharezone=self,
            is_active=True
        )

    def get_tool_list(self):
        """
        Get a list of all tools associated with this sharezone
        """
        return self.tool_set.filter(is_active=True)

    def get_available_tools(self):
        """
        Get a list of all available tools associated with this sharezone.
        """
        return self.tool_set.filter(
            is_active=True, 
            shared=True, 
            renter=None
        )

    def get_all_in_group(self, group):
        """
        Get a list of all active tools in a given ToolGroup.
        """
        return self.tool_set.filter(
            is_active=True,
            group=group
        )

    def get_admins(self):
        """
        Gets a queryset of all admins of this sharezone.
        """
        return User.objects.filter(
            is_active=True,
            profile__is_sharezone_admin=True,
            profile__sharezone=self,
            profile__is_approved=True
        )

    def get_non_admins(self):
        """
        Gets a queryset of all users of the sharezone who are not admins.
        """
        return User.objects.filter(
            is_active=True,
            profile__is_sharezone_admin=False,
            profile__sharezone=self,
            profile__is_approved=True
        )

    def approve(self):
        """
        Approve the sharezone
        """
        self.is_approved = True
        self.save()

    # No longer in use.
    def remove(self):
        """
        Remove the sharezone
        """
        self.is_active = False
        self.save()

    # Sharezone statistics functions.

    def get_most_recent_tool(self):
        """
        Returns the most recently used tool in this sharezone, based on most recent end date of a reservation.

        Returns - Tuple - (tool, most_recent_return_datetime)
        """
        reslist = Reservation.objects.filter(tool__sharezone=self, end_date__lte=timezone.now()).order_by('-end_date')
        if (reslist.count() > 0):
            return (reslist[0].tool, reslist[0].end_date)
        else:
            return None

    def get_most_used_tool(self):
        """
        Returns the most used tool from this sharezone

        Returns - Tuple - (tool, number_of_uses)
        """
        MAX = 0;
        best = None
        for tool in self.tool_set.all():
            res_len = Reservation.objects.filter(
                tool=tool, 
                tool__sharezone=self, 
                start_date__lte=timezone.now()
                ).count()
            if res_len > MAX:
                best = tool
                MAX = res_len
        return (best, MAX)

    def get_most_active_borrower(self):
        """
        Returns the user within this sharezone which has borrowed the
        most amount of tools.

        Returns - tuple - (user, number_of_borrows)
        """
        MAX = 0;
        borrower = None
        for user in User.objects.filter(
            profile__sharezone=self, 
            profile__is_approved=True
            ):
            borrows = Reservation.objects.filter(
                user=user, 
                tool__sharezone=self, 
                start_date__lte=timezone.now()
                ).count()
            if borrows > MAX:
                MAX = borrows
                borrower = user
        return (borrower, MAX)

    def get_most_active_lender(self):
        """
        Returns the user within the sharezone who has lent out the most amount
        of tools.

        Returns - tuple - (user, number_of_shares)
        """
        MAX = 0;
        lender = None
        for user in User.objects.filter(
            profile__sharezone=self, 
            profile__is_approved=True
            ):
            shares = Reservation.objects.filter(
                tool__owner=user, 
                tool__sharezone=self, 
                start_date__lte=timezone.now()
                ).count()
            if shares > MAX:
                MAX = shares
                lender = user
        return (lender, MAX)

    def get_number_of_shares(self):
        """
        Returns the total number of interactions in this sharezone

        Returns - int - number of interactions
        """
        return Reservation.objects.filter(tool__sharezone=self, start_date__lte=timezone.now()).count()

    def get_largest_sharezones(n = 5):
        """
        Gets the n largest sharezones.
        Returns a list of size n which will contain the sharezones.
        If there are not enough sharezones to fill the list the empty slots
        will be None
        """
        sharezone_list = []
        for sharezone in Sharezone.objects.filter(is_active=True):
            sharezone_list.append((sharezone, sharezone.get_user_list().count()))

        sharezone_list.sort(key=lambda x: -x[1])
        # Fill up the rest of the list with "None"s
        if len(sharezone_list) < n:
            sharezone_list.extend([None] * (n - len(sharezone_list)))
        return sharezone_list[0:n]


class UserProfile(models.Model):
    """
    Represents an individual user
    Extends the Django user model
    uses address model
    uses sharezone model
    """
    user = models.OneToOneField(User, related_name="profile")
    address = models.ForeignKey(Address)
    sharezone = models.ForeignKey(Sharezone, null=True, blank=True) #Sharezones are required
    is_approved = models.BooleanField("Approved?", default=False)
    is_sharezone_admin = models.BooleanField("Sharezone admin?", default=False)

    def __str__(self):
        """
        Basic string representation of a UserProfile
        """
        return self.user.username

    def notify(self):
        """
        If the user has a reservation that is less than a day away, send that
        user a message.
        """
        now = timezone.now()
        immediate_reservations = self.user.reservation_set.filter(
            end_date__gt=now, end_date__lt=now+datetime.timedelta(days=1),
            notified=False
            )
        if immediate_reservations.count() == 0:
            return False
        else:
            for res in immediate_reservations:
                sendReservationEndingMessage(res)
                res.notified=True
                res.save()
            return True


    def is_admin(self, sharezone=None):
        """
        Returns a boolean indicating whether or not the user is an admin.
        If sharezone is passed in, check if the user is an admin of that sharezone.
        Else, this is equivalent to user.is_superuser
        """
        # Ensure they are active and approved
        if (not (self.user.is_active and self.is_approved)):
            return False
        # Superusers administrate all sharezones
        if (self.user.is_superuser):
            return True
        # Next line fails if sharezone is None, no worries.
        elif (self.sharezone == sharezone and self.is_sharezone_admin):
            return True
        # Both cases fail, return False.
        return False

    def ban(self):
        """
        Bans the user associated with the user profile
        """
        if self.user.is_superuser:
            #You can't ban the super duper admin, silly
            return "no"
        user = self.user
        user.is_active = False # Prevents user from logging in
        user.profile.is_approved = False
        # Delete all sessions for the user
        [s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == user.id]
        # Save the user
        user.profile.save()
        user.save()

    def unban(self):
        """
        Unbans the user associated with the user profile
        """
        user = self.user
        user.is_active = True # Allows the user to log in
        # Save the user
        user.save()

    def approve(self):
        """
        Approve the user associated with the user profile
        """
        self.is_approved = True
        self.save()

    def make_sharezone_admin(self):
        """
        Makes a user into a sharezone admin
        """
        self.is_sharezone_admin = True
        self.save()

    def remove_sharezone_admin(self):
        """
        Makes a sharezone admin into a regular user
        """
        self.is_sharezone_admin = False
        self.save()


class ToolGroup(models.Model):
    """
    Represents a class of tools. E.G. Hammers, Wrenches, Screwdrivers, etc.
    Contains functionality to search the database for tools in a given group.
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        """
        Returns the name of the group
        """
        return self.name
    
    def get_best_tool(self, user):
        """
        Get the best tool that the user is able to borrow.
        """
        # We can safely assume that at this level all users have profiles
        tool_list = self.get_available_tools(user.profile.sharezone)
        if (tool_list.count() == 0):
            return None # No tools are available.
        return tool_list[0]

    def get_available_tools(self, sharezone=None):
        """
        Get a list of all tools in this group that are shared and are
        not removed. Sorted by quality. If sharezone is passed in, limit the
        search to that sharezone.
        """
        if sharezone is not None: #Sharezone was passed in, limit the search.
            return (sharezone.tool_set.filter(
                group=self,
                shared=True,
                is_active=True
                ).order_by('-quality'))

        return (Tool.objects.filter(
            group=self, 
            shared=True, 
            is_active=True
            ).order_by('-quality'))

    def get_all_tools(self, sharezone=None):
        """
        Get a list of all tools in the system that are in this group.
        Sorted by quality.
        """
        return Tool.objects.filter(
            group=self, 
            is_active=True
            ).order_by('-quality')

    def group_size(self):
        """
        returns the number of all active tools
        """
        return Tool.objects.filter(
            group=self, 
            is_active=True
            ).count()

    def get_largest_group():
        """
        Gets the largest group by active tools associated with that group.
        """
        groups = ToolGroup.objects.all()
        if groups.count() == 0:
            return None
        biggest_group = groups[0]
        for group in groups:
            if group.group_size() > biggest_group.group_size():
                biggest_group = group

        return biggest_group

    def get_average_tool_quality(self, sharezone=None):
        """
        Returns to the user the average tool quality for this group.
        Returns a double to the nearest tenths place.
        """
        quality_total = 0.0
        tool_list = self.get_available_tools(sharezone)
        if tool_list.count() == 0:
            return None
        for tool in tool_list:
            quality_total += tool.quality
        return round((quality_total / tool_list.count()), 1) # Returns the answer rounded to the tenths place


class Tool(models.Model):
    """
    Represents an individual tool object

    Fields:
    Variable  DataType:
    name        = String
    group       = ToolGroup
    owner       = User
    renter      = User
    Sharezone        = Sharezone
    quality     = int
    is_active   = Boolean
    shared      = Boolean
    description = String
    instruction = String
    """
    name = models.CharField(max_length=200)
    group = models.ForeignKey(ToolGroup)
    # reference a user's owned tools with User.ownedtool_set.all()
    owner = models.ForeignKey(User, related_name='ownedtool_set')
    # reference a user's rented tools with User.rentedtool_set.all()
    renter = models.ForeignKey(User, null=True, blank=True, 
        related_name='rentedtool_set')

    #NOTE: This should be changed when everything else has been
    sharezone = models.ForeignKey(Sharezone)
    quality = models.IntegerField('Quality (1-5)', default=3)
    is_active = models.BooleanField('Active?', default=True)
    shared = models.BooleanField('Shared?', default=True)
    # extra details about the tool
    description = models.CharField('Description', max_length=400, blank=True)
    instructions = models.CharField('Special Instructions', max_length=400, blank=True)

    def __str__(self):
        """
        Returns the string interpretation of tool (Star rating) + name
        """
        return "[" + self.quality_to_string() + "] " + self.name

    def can_be_borrowed(self):
        """
        Asks a tool if it can be borrowed
        returns a Boolean
        """    
        return (self.renter is None and self.shared and self.is_active)

    def is_on_loan(self):
        """
        Asks the tool if it is being loaned out
        returns a Boolean
        """
        return (self.renter is not None and self.is_active)
    
    def administrated_by(self, user):
        """
        Asks if the user is able to edit
        returns a Boolean
        """
        return (user.profile.is_admin(self.sharezone) or self.owner == user)

    def quality_to_string(self):
        """
        returns snazzy stars based on the quality of the tool
        """
        if self.quality > 5:
            self.quality = 5
            self.save()
        if self.quality < 1:
            self.quality = 1
            self.save()
        return self.quality * '★' + '☆' * (5-self.quality)

    def get_address(self):
        """
        Asks the tool what its address is
        returns the address of the tool's sharezone's address
        """
        return self.sharezone.address

    def is_held_by(self, user):
        """
        Returns True if the user currently has possession of the tool.
        """
        return (
            (self.renter is None and self.owner == user) or
            (self.renter == user))

    def get_future_reservations(self):
        return self.reservation_set.filter(
            end_date__gt=timezone.now()
        )

    def update(self):
        """
        Checks if there is a current reservation for the tool in question
        """
        reslist = Reservation.get_current(tool=self)
        if reslist.count() == 0:
            if self.renter is not None:
                self.renter = None
                self.save()
        else:
            if self.renter != reslist[0].user:
                self.renter = reslist[0].user
                self.save()

    def delete_future_reservations(self):
        """
        Removes all reservations that are in the future for this tool.
        """
        # First, end the current reservation.
        current_res = Reservation.get_current(tool=self)
        if current_res.count() != 0:
            current = current_res[0]
            current.end_date=timezone.now()
            self.renter = None
            current.save()
            self.save()

        # Now, find all future reservations and get rid of them.
        self.get_future_reservations().delete()
        # Have a nice day

    def viewable_by(self, user):
        """
        Checks if user is able to view the information about a tool.
        """
        # If the user is an approved member of this tool's sharezone, approve.
        if user.profile.sharezone == self.sharezone and user.profile.is_approved:
            return True
        # If the user is an admin or owns the tool, approve.
        elif self.administrated_by(user):
            return True
        # The user cannot view this page. Reject.
        return False

    # Static
    def update_all():
        """
        Update reservations for every tool in the system.
        """
        # reserved_tools = list(Tool.objects.filter(is_active=True))
        # Filtering is_active is bad, actually, fun fact.
        reserved_tools = list(Tool.objects.all())
        reslist = Reservation.get_current()
        for res in reslist:
            reserved_tools.remove(res.tool)
            if res.tool.renter != res.user:
                res.tool.renter = res.user
                res.tool.save()
        # all current reservations processed
        # remaining tools not reserved
        for tool in reserved_tools:
            if tool.renter is not None:
                tool.renter = None
                tool.save()



class Reservation(models.Model):
    """
    Class used for generating reservations of a tool
    """
    end_date = models.DateTimeField('End Date', default=timezone.now() + datetime.timedelta(days=14))
    start_date = models.DateTimeField('Start Date', default=timezone.now())
    tool = models.ForeignKey(Tool)
    user = models.ForeignKey(User)
    notified = models.BooleanField("Notified?", default=False)

    def __str__(self):
        return "%s: [%s] to [%s]" % (self.user, str(self.start_date), str(self.end_date))

    def is_valid(self):
        """
        True if no conflicting reservations and two weeks or less
        False otherwise
        """
        return (self.is_not_conflicting() and self.is_valid_length())

    def is_not_conflicting(self):
        """
        Returns True if there are no conflicting reservations for the
        same tool.
        """
        return (Reservation.objects.filter(
            tool=self.tool,
            end_date__gt=self.start_date,
            start_date__lt=self.end_date
            ).exclude(id=self.id).count() == 0)

    def is_too_old(self):
        """
        Tests if a reservation has a start date more than an hour in the past.
        Used for the ReservationForm
        """
        return ((self.start_date + datetime.timedelta(hours=1)) < timezone.now())

    def is_valid_length(self):
        """
        Ensures that the reservation is two weeks or less in length and the
        end date comes after the start date.
        """
        return (self.start_date < self.end_date and
            self.start_date + datetime.timedelta(days=14) >= self.end_date)

    def is_current(self):
        """
        Checks if a reservation is 'current'. (I.E. start date is before now,
        end date is after now.)
        """
        now = timezone.now()
        return (self.start_date <= now and 
            self.end_date > now)

    def get_current(tool=None):
        """
        Static method to get all current reservations. If Tool is specified,
        limit the search to that tool.
        """
        if tool is not None and not isinstance(tool, Tool):
            raise TypeError("Argument must be of type Tool")

        now = timezone.now()

        if tool:
            return tool.reservation_set.filter(
                start_date__lte=now,
                end_date__gt=now
                )

        return Reservation.objects.filter(
            start_date__lte=now,
            end_date__gt=now
            )
