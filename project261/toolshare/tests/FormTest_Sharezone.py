"""
File:       toolshare/FormTest_SharezoneForm.py
Language:   Python 3 with Django Web Framework

Author:     Val Booth <vxb4825@rit.edu>
Author:     Corban Mailloux <cdm3806@rit.edu>
Author:     Adam McCarthy <aem1269@rit.edu>
Author:     Michael Washburn <mdw7326@rit.edu>
Author:     Bryon Wilkins <brw4824@rit.edu>

"""

from django.test import TestCase
from ..forms import SharezoneForm

class SharezoneFormTest(TestCase):
    """
    Tests to make sure the SharezoneForm is valid if a name is given
    or if a name AND description is given.
    """

    def setUp(self):
        self.content = {
            "name" : "Test Sharezone",
            "description" : "Test description",
            }

    def test_standard_valid(self):
        """
        Tests to make sure a standard input (name and description given)
        is valid and accepted by the form.
        """
        form = SharezoneForm(self.content)
        self.assertTrue(form.is_valid())

    def test_name_only(self):
        """
        Tests to make sure the form is valid when given only a name.
        """
        del self.content['description'] #deletes the description from content.
        form = SharezoneForm(self.content)
        self.assertTrue(form.is_valid())

    def test_description_only(self):
        """
        Tests to make sure that a form containing only a description is not valid.
        """
        del self.content['name']
        form = SharezoneForm(self.content)
        self.assertFalse(form.is_valid())

    def test_no_content(self):
        """
        Tests to make sure that an empty form is not valid.
        """
        form = SharezoneForm()
        self.assertFalse(form.is_valid())
