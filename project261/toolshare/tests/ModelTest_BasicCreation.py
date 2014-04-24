"""
File:       toolshare/tests/ModelCreationTests.py
Language:   Python 3 with Django Web Framework

Author:     Val Booth <vxb4825@rit.edu>
Author:     Corban Mailloux <cdm3806@rit.edu>
Author:     Adam McCarthy <aem1269@rit.edu>
Author:     Michael Washburn <mdw7326@rit.edu>
Author:     Bryon Wilkins <brw4824@rit.edu>

"""

from django.test import TestCase
from ..models import *
from django.contrib.auth.models import User
from .testutils import *

class ModelCreationTests(TestCase):

    def setUp(self):
        """
        Defines data for use to create models
        """
        self.line1 = "42 Testers Avenue"
        self.line2 = "Appartment # 9 3/4"
        self.zipcode = "12345"

    def test_Address(self):
        """
        This function will test to make sure that the Address 'object' can be created
        and stored in the database. It will also make sure the zip code is allocated 
        just enough space (5 characters).
        """
        Address.objects.create(line1=self.line1,line2=self.line2,zip=self.zipcode) #creates Address

        #retrieves object
        address = Address.objects.filter(line1=self.line1)[0]

        self.assertEqual(self.line2, address.line2)
        self.assertEqual(self.zipcode, address.zip)

    def test_UserProfile(self):
        """
        This function will test the creation of a UserProfile. It neglects to use 
        a real sharezone as these tests are being designed to start from the bottom and work
        their way up. Because sharezone has not been tested yet, we neglect it.
        """
        user = User.objects.create(username="tester",password="password")
        address = Address.objects.create(line1=self.line1,line2=self.line2,zip=self.zipcode)
        UserProfile.objects.create(address=address,user=user,sharezone=None)

        profile = user.profile

        self.assertEqual(address,profile.address)
        self.assertEqual(user,profile.user)

    def test_ToolGroup(self):
        """
        This function tests the creation of the ToolGroup class. 
        """
        group = ToolGroup.objects.create(name="Hammers")
        self.assertEqual(group,ToolGroup.objects.filter(name="Hammers")[0])

    def test_Tool(self):
        """
        This function tests the basic creation of a tool with a sharezone and no current
        renter
        """
        # address = Address.objects.create(line1=self.line1,line2=self.line2,zip=self.zipcode)
        # owner = User.objects.create(username="owner",password="password")
        # sharezone = None
        # owner_profile = UserProfile.objects.create(user=owner,address=address,sharezone=sharezone)
        # group = ToolGroup.objects.create(name="Hammers")
        group = create_toolgroup()
        owner = create_user(address=create_address(line1=self.line1, line2=self.line2,
            zip=self.zipcode))
        sharezone = create_sharezone()
        tool = Tool.objects.create(name="Test Hammer",group=group,owner=owner,renter=None,sharezone=sharezone)
        #make sure the tool exists
        self.assertEqual(tool,Tool.objects.filter(name="Test Hammer")[0])

    def test_Sharezone(self):
        """
        Creates a sharezone object and attempts to retrieve it from the database
        """
        user = create_user(username="tester",password="password", is_sharezone_admin=True)
        address = Address.objects.create(line1=self.line1,line2="",zip=self.zipcode)
        Sharezone.objects.create(address=address)
        sharezone = Sharezone.objects.get(address=address)
        self.assertTrue(user.profile.is_sharezone_admin)
        self.assertEqual(address,sharezone.address)

    def test_Reservation(self):
        """
        Tests the basic construction of the Reservation model while taking advantage
        of its default parameters
        """
        user = User.objects.create(username="tester",password="password")
        address = Address.objects.create(line1=self.line1,line2="",zip=self.zipcode)
        sharezone = Sharezone.objects.create(address=address)
        group = ToolGroup.objects.create(name="Hammers")
        tool = Tool.objects.create(name="Test Hammer",group=group,owner=user,renter=None,sharezone=sharezone)

        Reservation.objects.create(tool=tool,user=user)
        res = Reservation.objects.filter(tool=tool)[0]

        self.assertEqual(tool,res.tool)
        self.assertEqual(user,res.user)
        