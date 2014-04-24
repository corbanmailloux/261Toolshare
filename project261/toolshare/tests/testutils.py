"""
File:       toolshare/tests/testutils.py
Language:   Python 3 with Django Web Framework

Author:     Val Booth <vxb4825@rit.edu>
Author:     Corban Mailloux <cdm3806@rit.edu>
Author:     Adam McCarthy <aem1269@rit.edu>
Author:     Michael Washburn <mdw7326@rit.edu>
Author:     Bryon Wilkins <brw4824@rit.edu>

A set of helper functions to simplify the creation of database objects
for testing purposes.
"""
from ..models import *
from django.utils import timezone
import datetime
from django.core.urlresolvers import reverse

class Static():
    """
    Holds counters for the various models. Helps create names.
    """
    user_count = User.objects.count() + 1;
    address_count = Address.objects.count() + 1;
    group_count = ToolGroup.objects.count() + 1;
    tool_count = Tool.objects.count() + 1;
    sharezone_count = Sharezone.objects.count() + 1;
    reservation_count = Reservation.objects.count() + 1;

def login_client(client, user=None):
    if user == None:
        user = create_user()
    return client.post(reverse('login'),{"username":user.username, "password":user.password})

def create_live_user(username=None, password=None, email=None, address=None,
    sharezone=None, is_sharezone_admin=False, is_approved=True, is_superuser=False):
    """
    Create a user which can be used in views. This is here because it needs to 
    use create_user() instead of create(). create() is faster but users created 
    with this cannot be used to login with the test client. So to increase the 
    speed tests are run, this will be used ONLY for testing views.
    """
    if username is None:
        username = "user%d" % Static.user_count
        while User.objects.filter(username=username).count() != 0:
            Static.user_count += 1
            username = "user%d" % Static.user_count
    if password is None:
        password = "password"
    if email is None:
        email="user%d@test.com" % Static.user_count

    Static.user_count += 1
    user = User.objects.create_user(username=username, password=password)
    user.is_superuser = is_superuser
    user.save()
    
    if address is None:
        address=create_address()
    if sharezone is None:
        sharezone=create_sharezone()
    UserProfile.objects.create(user=user, address=address, sharezone=sharezone,
        is_sharezone_admin=is_sharezone_admin, is_approved=is_approved)
    return user

def create_user(username=None, password=None, email=None, address=None,
    sharezone=None, is_sharezone_admin=False, is_approved=True, is_superuser=False):
    """
    Create a user. If username or password are specified, use them.
    Otherwise create serialized ones. Checks for already existing users
    and ensures the names don't conflict.
    """
    if username is None:
        username = "user%d" % Static.user_count
        while User.objects.filter(username=username).count() != 0:
            Static.user_count += 1
            username = "user%d" % Static.user_count
    if password is None:
        password = "password"
    if email is None:
        email="user%d@test.com" % Static.user_count

    Static.user_count += 1
    user = User.objects.create(username=username, password=password, is_superuser=is_superuser)
    
    if address is None:
        address=create_address()
    if sharezone is None:
        sharezone=create_sharezone()
    UserProfile.objects.create(user=user, address=address, sharezone=sharezone,
        is_sharezone_admin=is_sharezone_admin, is_approved=is_approved)
    return user

def create_address(line1=None, line2=None, zip=None):
    """
    Creates an Address object. If line1 is not provided, creates a serialized
    line1 (5 test lane, 6 test lane, etc). If zip is not provided, uses 12345.
    """
    if line1 is None:
        line1 = "%d Test Lane" % Static.address_count
    if line2 is None:
        line2 = "Apartment A"
    if zip is None:
        zip = "12345"

    Static.address_count += 1
    return Address.objects.create(line1=line1, line2=line2, zip=zip)

def create_sharezone(name=None, address=None, description=""):
    """
    Creates a Sharezone object. If name is not provided, creates a serialized name
    (Sharezone 1, Sharezone 2, etc). Creates address if not provided.
    """
    if name is None:
        name = "Sharezone %d" % Static.sharezone_count
    if address is None:
        address = create_address()

    Static.sharezone_count += 1
    return Sharezone.objects.create(name=name, address=address, description=description)

def create_toolgroup(name=None):
    """
    Creates a ToolGroup object. If name is not provided, creates a serialized
    name (Test Group 1, Test Group 2, etc).
    """
    if name is None:
        name = "Test Group %d" % Static.group_count

    Static.group_count += 1
    return ToolGroup.objects.create(name=name)

def create_tool(name=None, group=None, owner=None, renter=None, sharezone=None,
    quality=3, is_active=True, shared=True, description="",
    instructions=""):
    """
    Creates a Tool object. If name is not provided, creates a serialized name
    (Tool 1, Tool 2, etc). Creates all other non-provided required fields.
    """
    if name is None:
        name = "Tool %d" % Static.tool_count
    if group is None:
        group = create_toolgroup()
    if owner is None:
        owner = create_user()
    if sharezone is None:
        sharezone = create_sharezone()

    Static.tool_count += 1
    return Tool.objects.create(name=name, group=group, owner=owner, 
        renter=renter, sharezone=sharezone, quality=quality, is_active=is_active,
        shared=shared, description=description, instructions=instructions)

def create_reservation(user=None, tool=None, start_date=None, end_date=None):
    """
    Creates a new Reservation object. Creates all non-provided fields. Start
    date is assumed to be now, reservation length is assumed to be 14 days.
    """
    now = timezone.now()
    if user is None:
        user = create_user()
    if tool is None:
        tool = create_tool()
    if start_date is None:
        start_date = now
    if end_date is None:
        end_date = start_date + datetime.timedelta(days=14)

    Static.reservation_count += 1
    return Reservation.objects.create(user=user, tool=tool, 
        start_date=start_date, end_date=end_date)