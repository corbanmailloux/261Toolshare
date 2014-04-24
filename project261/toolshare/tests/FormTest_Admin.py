"""
File:       toolshare/FormTest_Admin.py
Language:   Python 3 with Django Web Framework

Author:     Val Booth <vxb4825@rit.edu>
Author:     Corban Mailloux <cdm3806@rit.edu>
Author:     Adam McCarthy <aem1269@rit.edu>
Author:     Michael Washburn <mdw7326@rit.edu>
Author:     Bryon Wilkins <brw4824@rit.edu>

"""

from django.test import TestCase
from ..forms import AdminUserForm, AdminProfileForm, AdminApproveSharezoneForm

class AdminFormTests(TestCase):
    """
    This class tests the forms dealing with Administrative Editing.
    form1 will refer to AdminUserForm
    form2 will refer to AdminProfileForm
    form3 will refer to AdminApproveSharezoneForm
    """

    def setUp(self):
        """
        Initialize form information.
        """
        self.content = {
            'is_approved' : True,
            'is_sharezone_admin' : True,
            'is_active' : True,
            'is_superuser' : True,
            }

    def test_standard_valid(self):
        """
        Tests to make sure when the forms are given a basic
        input they work.
        """
        form1 = AdminUserForm(self.content)
        self.assertTrue(form1.is_valid())

        form2 = AdminProfileForm(self.content)
        self.assertTrue(form2.is_valid())

        form3 = AdminApproveSharezoneForm(self.content)
        self.assertTrue(form3.is_valid())

    def test_all_empty(self):
        """
        Tests to make sure the forms cannot be completely empty.
        """
        form1 = AdminUserForm()
        self.assertFalse(form1.is_valid())

        form2 = AdminProfileForm()
        self.assertFalse(form2.is_valid())

        form3 = AdminApproveSharezoneForm()
        self.assertFalse(form3.is_valid())

    def test_is_approved_empty(self):
        """
        Tests to make sure that form2 and form3 are valid
        only without is_approved and that it goes to the correct
        default value, False.
        """
        del self.content['is_approved']

        form2 = AdminProfileForm(self.content)
        self.assertTrue(form2.is_valid())

        #test to make sure the default is False.
        profile = form2.save(commit=False)
        self.assertFalse(profile.is_approved)

        form3 = AdminApproveSharezoneForm(self.content)
        self.assertTrue(form3.is_valid())

        #test to make sure default is false
        sharezone = form3.save(commit=False)
        self.assertFalse(sharezone.is_approved)

    def test_is_sharezone_admin_empty(self):
        """
        Tests to make sure that form2 is still valid when 
        there is only no sharezone admin. Also tests to make sure
        that it goes to its default value, False.
        """
        del self.content['is_sharezone_admin']
        form2 = AdminProfileForm(self.content)
        self.assertTrue(form2.is_valid())

        #test to make sure the default is False.
        profile = form2.save(commit=False)
        self.assertFalse(profile.is_sharezone_admin)

    def test_is_active_empty(self):
        """
        Tests to make sure that AdminUserForm is valid with no is_active field.
        It also makes sure the default of is_active is False.
        """
        del self.content['is_active']
        form1 = AdminUserForm(self.content)
        self.assertTrue(form1.is_valid())

        #test the default value of is_active
        user = form1.save(commit=False)
        self.assertFalse(user.is_active)

    def test_is_superuser_empty(self):
        """
        Tests to make sure that the is_superuser field can be empty
        and that the default when It is empty is False.
        """
        del self.content['is_superuser']
        form1 = AdminUserForm(self.content)
        self.assertTrue(form1.is_valid())

        #test the default value of is_active
        user = form1.save(commit=False)
        self.assertFalse(user.is_superuser)

