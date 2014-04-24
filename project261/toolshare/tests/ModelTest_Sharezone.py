"""
File:       toolshare/tests/ModelTest_Sharezone.py
Language:   Python 3 with Django Web Framework

Author:     Val Booth <vxb4825@rit.edu>
Author:     Corban Mailloux <cdm3806@rit.edu>
Author:     Adam McCarthy <aem1269@rit.edu>
Author:     Michael Washburn <mdw7326@rit.edu>
Author:     Bryon Wilkins <brw4824@rit.edu>

Tests the functionality included in the toolshare.models.Sharezone class
"""

from django.test import TestCase
from ..models import *
from .testutils import *
from django.contrib.auth.models import User

class SharezoneTests(TestCase):
    """
    Tests functions of the sharezone class to make sure they return the correct information
    and follow the correct logic.
    """

    def setUp(self):
        """
        Initializes data for the following tests
        """
        self.zipcode = "12345"
        #initialize sharezone_admin address and user
        sharezone_admin_address = Address.objects.create(line1="42 Wallaby Way", line2="",zip=self.zipcode)
        self.sharezone_admin = User.objects.create(username="tester",password="password")
        #initialize sharezone
        sharezone_address = Address.objects.create(line1="45 Wallaby Way",line2="",zip=self.zipcode)
        self.sharezone = Sharezone.objects.create(address=sharezone_address)
        #add sharezone to sharezone_admin's profile
        self.sharezone_admin_profile = UserProfile.objects.create(user=self.sharezone_admin,
            address=sharezone_admin_address,sharezone=self.sharezone,is_sharezone_admin=True, is_approved=True)

        self.group = ToolGroup.objects.create(name="Hammers")

        #populate the sharezone with users and tools
        self.number_of_users = 3 #doesn't include the sharezone_admin yet
        for x in range(1,self.number_of_users+1): 
            address = Address.objects.create(line1 = str(45 + x) + "Wallaby Way",line2="",zip=self.zipcode)
            user = User.objects.create(username="user"+str(x),password="password")
            profile = UserProfile.objects.create(address=address,user=user,sharezone=self.sharezone, is_approved=True)
            group = ToolGroup.objects.create(name="Hammers")
            tool = Tool.objects.create(name="Hammer #"+str(x),group=self.group,owner=user,renter=None,sharezone=self.sharezone)
        self.number_of_users += 1 #to account for the sharezone_admin

    def test_get_user_list(self):
        """
        Tests to make sure the user_list is the correct length
        """
        self.assertEqual(self.number_of_users,self.sharezone.get_user_list().count())

    def test_get_tool_list(self):
        """
        Tests to make sure the correct amount of tools is returned in the tool list.
        This accounts for the fact that the sharezone_admin was not given a tool upon the 
        setUp of users, and all other users have 1 and only 1 tool
        """
        self.assertEqual(self.number_of_users-1,self.sharezone.get_tool_list().count())

    def test_get_available_tools(self):
        """
        Tests to make sure the correct number of available tools is given. 
        This relies on the fact that at the start of this test each user (except
        the sharezone_admin) has exactly 1 tool, and all tools are available.
        """
        self.assertEqual(self.number_of_users-1,self.sharezone.get_available_tools().count())

        #make 1 more tool unavailable.
        tool = Tool.objects.filter(sharezone=self.sharezone)[0]
        tool.shared = False
        tool.save()

        self.assertEqual(self.number_of_users-2,self.sharezone.get_available_tools().count())

    def test_get_all_in_group(self):
        """
        This test relies on the fact that every tool is in the Hammers ToolGroup
        It will check to make sure all the tools are accounted for in retrieving
        all members of the group. It also relies on the fact that all users except
        the sharezone_admin have a tool.
        """
        self.assertEqual(self.number_of_users-1, self.sharezone.get_all_in_group(self.group).count())

    def test_tostring(self):
        """
        Simple test of the __str__() method of Sharezones.
        """
        sharezone = create_sharezone(name="Test Sharezone Number 1")
        self.assertEqual(str(sharezone), "Test Sharezone Number 1")

    def test_get_admins(self):
        """
        Tests the get_admins method of a sharezone
        """
        sharezone = create_sharezone(name="Test Sharezone Number 2")
        user1 = create_user(username="not_admin", sharezone=sharezone, is_sharezone_admin=False)
        user2 = create_user(username="admin1", sharezone=sharezone, is_sharezone_admin=True)
        user3 = create_user(username="admin2", sharezone=sharezone, is_sharezone_admin=True)

        admins = str(sharezone.get_admins())
        self.assertTrue("admin1" in admins)
        self.assertTrue("admin2" in admins)
        self.assertFalse("not_admin" in admins)

    def test_get_admins_with_no_admins(self):
        """
        When there are no admins, get_admins should return an empty queryset.
        """
        sharezone = create_sharezone(name="Test Sharezone Number 3")
        create_user(username="user_1", sharezone=sharezone, is_sharezone_admin=False)
        create_user(username="user_2", sharezone=sharezone, is_sharezone_admin=False)
        create_user(username="user_3", sharezone=sharezone, is_sharezone_admin=False)

        admins = str(sharezone.get_admins())
        self.assertFalse("user1" in admins)
        self.assertFalse("user2" in admins)
        self.assertFalse("user3" in admins)

    def test_get_non_admins(self):
        """
        Tests the get_non_admins method of a sharezone
        """
        sharezone = create_sharezone(name="Test Sharezone Number 4")
        create_user(username="user_1", sharezone=sharezone, is_sharezone_admin=False)
        create_user(username="admin1", sharezone=sharezone, is_sharezone_admin=True)
        create_user(username="admin2", sharezone=sharezone, is_sharezone_admin=True)

        non_admins = str(sharezone.get_non_admins())
        self.assertFalse("admin1" in non_admins)
        self.assertFalse("admin2" in non_admins)
        self.assertTrue("user_1" in non_admins)

    def test_get_non_admins_with_no_admins(self):
        """
        Tests the get_non_admins method of a sharezone when there are no sharezone admins
        """        
        sharezone = create_sharezone(name="Test Sharezone Number 5")
        create_user(username="user_1", sharezone=sharezone, is_sharezone_admin=False)
        create_user(username="user_2", sharezone=sharezone, is_sharezone_admin=False)
        create_user(username="user_3", sharezone=sharezone, is_sharezone_admin=False)

        non_admins = str(sharezone.get_non_admins())
        self.assertTrue("user_1" in non_admins)
        self.assertTrue("user_2" in non_admins)
        self.assertTrue("user_3" in non_admins)

    def test_get_non_admins_with_no_non_admins(self):
        """
        Tests the get_non_admins method of a sharezone when all sharezone users are admins
        """
        sharezone = create_sharezone(name="Test Sharezone Number 6")
        create_user(username="user_1", sharezone=sharezone, is_sharezone_admin=True)
        create_user(username="user_2", sharezone=sharezone, is_sharezone_admin=True)
        create_user(username="user_3", sharezone=sharezone, is_sharezone_admin=True)

        self.assertEqual(sharezone.get_non_admins().count(), 0)
        non_admins = str(sharezone.get_non_admins())
        self.assertFalse("user_1" in non_admins)
        self.assertFalse("user_2" in non_admins)
        self.assertFalse("user_3" in non_admins)

    def test_get_most_used_tool(self):
        """
        Tests the get_most_used_tool function. this function is used for 
        sharezone statistics.
        """
        tool = Tool.objects.all()[0]
        Reservation.objects.create(tool=tool, user= self.sharezone_admin)
        self.assertEqual(tool, self.sharezone.get_most_used_tool()[0])

    def test_get_most_active_borrower(self):
        """
        Makes a user borrow several tools and checks to make sure that 
        this user is returned by the get_most_active_borrower function.
        """
        #the user will borrow two tools.
        user = User.objects.all()[0]
        for tool in Tool.objects.all()[:2]:
            Reservation.objects.create(tool=tool, user=user)
        self.assertTrue(user, self.sharezone.get_most_active_borrower()[0])

    def test_get_most_active_lender(self):
        """
        This function will have a user borrow a tool and check
        to make sure the owner of the tool is returned by
        the get_most_active_lender function.
        """
        tool = Tool.objects.all()[0]
        lender = tool.owner
        borrower = User.objects.exclude(username=lender.username)[0]
        Reservation.objects.create(user=borrower,tool=tool)
        self.assertEqual(lender, self.sharezone.get_most_active_lender()[0])
        self.assertNotEqual(borrower, self.sharezone.get_most_active_lender()[0])

    def test_get_number_of_shares(self):
        """
        Returns the total number of transactions in this sharezone.
        """
        self.assertEqual(0,self.sharezone.get_number_of_shares())

        user = User.objects.all()[0]
        tool = Tool.objects.all()[0]
        Reservation.objects.create(user=user,tool=tool)

        self.assertEqual(1, self.sharezone.get_number_of_shares())

    def test_get_largest_sharezones(self):
        """
        Test to make sure that self.sharezone is returned by get_largest_sharezones 
        with an argument of n=1.
        """
        self.assertEqual(self.sharezone, Sharezone.get_largest_sharezones(n=1)[0][0])

