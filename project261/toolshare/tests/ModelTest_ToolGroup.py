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

class ToolGroupTests(TestCase):
    """
    Tests the in-class functions of ToolGroup. The setUp method will construct
    data and objects to call the funtions on.
    """

    def setUp(self):
        """
        Initializes data for use in tests
        """
        self.group = ToolGroup.objects.create(name="Hammers")
        self.group2 = ToolGroup.objects.create(name="Screwdrivers")
        self.sharezone = create_sharezone()
        #initialize a user to own tools
        self.user = User.objects.create(username="tester",password="password")
        address = Address.objects.create(line1="23 Test Drive", line2="",zip="12345")
        self.profile = UserProfile.objects.create(user=self.user,address=address,sharezone=self.sharezone)

        #construct tools for the Hammers group
        self.number_of_tools = 3
        for x in range(1,self.number_of_tools + 1):
            Tool.objects.create(name="Hammer"+str(x),group=self.group,owner=self.user,sharezone=self.sharezone)

    def test_get_best_tool(self):
        """
        Sets one tool to have a higher quality than the rest. It then checks to make
        sure the correct tool is returned from the function.
        """
        #change one tool to have a higher quality
        tool = Tool.objects.filter(group=self.group)[0]
        tool.quality = 5
        tool.save()

        #make sure this is the tool returned by get_best_tool
        self.assertEqual(tool,self.group.get_best_tool(self.user))
        #make sure if there are no tools none is returned
        self.assertEqual(None,self.group2.get_best_tool(self.user))

    def test_get_available_tools(self):
        """
        Gets a list of all the tools created in the setup and makes sure they
        are returned here. Also makes sure unshared tools and  not active tools
        are not displayed.
        """
        #get list of all tools (all the tools added are currently shared and active)
        tool_list = list(Tool.objects.filter(group=self.group))
        #add a not shared tool
        Tool.objects.create(name="Not Shared Hammer",group=self.group,owner=self.user,sharezone=self.sharezone,shared=False)
        #add a non-active tool
        Tool.objects.create(name="Not Active Hammer",group=self.group,owner=self.user,sharezone=self.sharezone,is_active=False)
        #make sure only the shared and active tools are returned.
        self.assertEqual(self.number_of_tools,self.group.get_available_tools().count())

        #make sure an empty list is returned when there are no tools.
        self.assertFalse(self.group2.get_available_tools())

    def test_get_all_tools(self):
        """
        Tests to make sure all the tools are returned by the get_all_tools function
        """
        tool_list = Tool.objects.filter(group=self.group,is_active=True)
        self.assertTrue(tool_list,self.group.get_all_tools())
        #make sure an empty list is returned when there are no tools
        self.assertFalse(self.group2.get_all_tools())

    def test_group_size(self):
        """
        Makes sure only active group members are counted in group_size
        """
        tool_list = Tool.objects.filter(group=self.group,is_active=True)
        self.assertEqual(tool_list.count(),self.group.group_size())
        #make sure that 0 is returned by the lack of tools in a group
        self.assertEqual(0,self.group2.group_size())

    def test_get_largest_group(self):
        """
        Makes sure that self.group1 is returned by the get_largest_group
        function.
        """
        self.assertEqual(self.group, ToolGroup.get_largest_group())
        self.assertNotEqual(self.group2, ToolGroup.get_largest_group())

    def test_get_average_tool_quality(self):
        """
        Because all the tools are created with the default quality=3,
        the average tool quality should be 3.
        """
        self.assertEqual(3, self.group.get_average_tool_quality())
