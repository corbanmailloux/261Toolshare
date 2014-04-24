"""
File:       toolshare/FormTest_User.py
Language:   Python 3 with Django Web Framework

Author:     Val Booth <vxb4825@rit.edu>
Author:     Corban Mailloux <cdm3806@rit.edu>
Author:     Adam McCarthy <aem1269@rit.edu>
Author:     Michael Washburn <mdw7326@rit.edu>
Author:     Bryon Wilkins <brw4824@rit.edu>

"""

from django.test import TestCase
from ..forms import ToolForm, EditToolQualityForm
from .testutils import *

class ToolFormTests(TestCase):
    """
    This class will test to make sure that all ModelForms dealing
    with Tools accept the correct forms of input for their fields.

    form1 will refer to ToolForm
    form2 will refer to EditToolQualityForm
    """

    def setUp(self):
        """
        Initialize form data.
        """
        self.content = {
            'name':'test hammer',
            'group':create_toolgroup().id,
            'quality':3,
            'shared':True,
            'owner': create_user().id,
            'description': "Test description",
            'instructions': "Test instructions",
            }

    def test_standard_valid(self):
        """
        Tests a standard form input.
        """
        form1 = ToolForm(self.content)
        self.assertTrue(form1.is_valid())

        form2 = EditToolQualityForm(self.content)
        self.assertTrue(form2.is_valid())

    def test_empty(self):
        """
        Tests to make sure empty forms aren't valid.
        """ 
        form1 = ToolForm()
        self.assertFalse(form1.is_valid())

        form2 = EditToolQualityForm()
        self.assertFalse(form2.is_valid())

    def test_name_empty(self):
        """
        Tests to make sure the name field cannot be empty.
        """
        del self.content['name']
        form1 = ToolForm(self.content)
        self.assertFalse(form1.is_valid())

    def test_group_empty(self):
        """
        Tests to make sure the group field cannot be empty.
        """
        del self.content['group']
        form1 = ToolForm(self.content)
        self.assertFalse(form1.is_valid())

    def test_quality_empty(self):
        """
        Tests to make sure the quality of a tool cannot
        be empty.
        """
        del self.content['quality']
        form1 = ToolForm(self.content)
        self.assertFalse(form1.is_valid())

        form2 = EditToolQualityForm(self.content)
        self.assertFalse(form2.is_valid())

    def test_quality_zero(self):
        """
        Tests to make sure quality cannot be 0.
        """
        self.content['quality'] = 0
        form1 = ToolForm(self.content)
        self.assertFalse(form1.is_valid())

        form2 = EditToolQualityForm(self.content)
        self.assertFalse(form2.is_valid())

    def test_quality_six(self):
        """
        Tests to make sure the quality cannot excede its 
        upper bound, 5.
        """
        self.content['quality'] = 6
        form1 = ToolForm(self.content)
        self.assertFalse(form1.is_valid())

        form2 = EditToolQualityForm(self.content)
        self.assertFalse(form2.is_valid())

    def test_shared_empty(self):
        """
        Tests to make sure the shared field CAN be empty.
        An empty shared field should default to False.
        """
        del self.content['shared']
        form1 = ToolForm(self.content)
        self.assertTrue(form1.is_valid())

        #make sure the shared attribute is False
        tool = form1.save(commit=False)
        self.assertFalse(tool.shared)

    def test_description_empty(self):
        """
        Tests to make sure the description CAN be empty.
        """
        del self.content['description']
        form1 = ToolForm(self.content)
        self.assertTrue(form1.is_valid())

    def test_instructions_empty(self):
        """
        Tests to make sure the tool instructions CAN be empty.
        """
        del self.content['instructions']
        form1 = ToolForm(self.content)
        self.assertTrue(form1.is_valid())