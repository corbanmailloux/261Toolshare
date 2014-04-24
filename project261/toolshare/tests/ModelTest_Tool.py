"""
File:       toolshare/tests/ModelTest_Tool.py
Language:   Python 3 with Django Web Framework

Author:     Val Booth <vxb4825@rit.edu>
Author:     Corban Mailloux <cdm3806@rit.edu>
Author:     Adam McCarthy <aem1269@rit.edu>
Author:     Michael Washburn <mdw7326@rit.edu>
Author:     Bryon Wilkins <brw4824@rit.edu>

A set of test cases to test functionality and creation of Tool objects.
"""

from django.test import TestCase
from ..models import *
from .testutils import *
from django.contrib.auth.models import User
from django.utils import timezone

class ToolTests(TestCase):
    """
    Test the in-class functions of the Tool Class. This will create test data then
    execute the functions in Tool, then check the results with expected results.
    """

    def setUp(self):
        """
        Initializes neccessary data for use in tests. This will create tools, users,
        a sharezone, and addresses!
        """
        #initialize addresses
        zipcode = "12345"
        address1 = Address.objects.create(line1="24 Test Drive",zip=zipcode)
        address2 = Address.objects.create(line1="25 Test Drive",zip=zipcode)
        address3 = Address.objects.create(line1="26 Test Drive",zip=zipcode)
        address4 = Address.objects.create(line1="27 Test Drive",zip=zipcode)
        addresses = [address1,address2,address3,address4]

        #initialize two normal users, and an admin
        self.user1 = create_user()
        self.user2 = create_user()
        self.admin = create_user(is_superuser=True)

        #create a sharezone for the sharezone
        self.sharezone = Sharezone.objects.create(address=address4)
        self.sharezone_admin = create_user(username="sharezone_admin",password="password", is_sharezone_admin=True, sharezone=self.sharezone)
        users = [self.user1,self.user2,self.admin,self.sharezone_admin]

        #create a ToolGroup
        self.group = ToolGroup.objects.create(name="Hammers")

        #create a ToolGroup
        self.group = ToolGroup.objects.create(name="Hammers")

        #create a tool for user1
        self.tool = Tool.objects.create(name="Hammer",group=self.group,owner=self.user1,sharezone=self.sharezone)

    def test_can_be_borrowed(self):
        """
        Tests to make sure the tool, in its current state can be borrowed. Then it 
        will toggle is_active and make sure it cannot. Then it will create a
        reservation and make sure the tool cannot be borrowed.
        """
        self.assertTrue(self.tool.can_be_borrowed())

        self.tool.is_active = False
        self.assertFalse(self.tool.can_be_borrowed())
        self.tool.is_active = True

        self.tool.renter = self.user2
        self.tool.save()
        self.assertFalse(self.tool.can_be_borrowed())
        self.tool.renter = None
        self.tool.save()
        

    def test_is_on_loan(self):
        """
        Checks to make sure that the is_on_loan function returns True
        only when another person other than the owner has possession of it.
        """
        self.assertFalse(self.tool.is_on_loan())

        self.tool.renter = self.user2
        self.tool.save()
        self.assertTrue(self.tool.is_on_loan())
        self.tool.renter = None
        self.tool.save()

    def test_administrated_by(self):
        """
        Tests to make sure the tool is administrated by user1(owner), the sharezone admin,
        and the administrator. But NOT user2
        """
        self.assertTrue(self.tool.administrated_by(self.user1))
        self.assertTrue(self.tool.administrated_by(self.sharezone_admin))
        self.assertTrue(self.tool.administrated_by(self.admin))
        self.assertFalse(self.tool.administrated_by(self.user2))

    def test_get_address(self):
        """
        Tests the Tool.get_address() method
        """
        self.assertEqual(self.sharezone.address,self.tool.get_address())

    def test_is_held_by(self):
        """
        Tests to make sure that this function returns true if the user is in possession 
        of the tool. If a user borrows the tool, it will return true for him. If the user
        is the owner, and the tool is not borrowed and the tool is shared from home it
        will return True.
        """
        #There is no renter for self.tool, and it is owned by self.user1.
        self.assertTrue(self.tool.is_held_by(self.user1))

        #user 2 does not have the tool
        self.assertFalse(self.tool.is_held_by(self.user2))

        self.tool.renter = self.user2
        self.tool.save()
        #now user2 does have the tool
        self.assertTrue(self.tool.is_held_by(self.user2))