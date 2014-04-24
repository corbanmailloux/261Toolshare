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
from ..forms import UserForm, EditUserForm

class UserFormTests(TestCase):
    """
    This class ensures that user forms are valid only
    when all the fields are properly filled.

    This will test UserForm and EditUserForm
    Note: form1 will refer to UserForm and form2
    will refer to EditUserForm
    """

    def setUp(self):
        """
        create test data for use in the form.
        Tests will then delete or modify data as needed
        by changing the value using content[key] = newValue
        or deleting it with del content[key].
        """
        self.content = {
            'username' : 'testuser',
            'first_name' : 'Tester',
            'last_name' : 'Testington',
            'email' : 'test@test.com',
            'password1' : 'password',
            'password2' : 'password',
            }

    def test_standard_valid(self):
        """
        Tests a standard valid input with all fields correct.
        """
        form1 = UserForm(self.content)
        self.assertTrue(form1.is_valid())

        form2 = EditUserForm(self.content)
        self.assertTrue(form1.is_valid())

    def test_empty_form(self):
        """
        Tests to make sure an empty form is not validated.
        """
        form1 = UserForm()
        self.assertFalse(form1.is_valid())

        form2 = EditUserForm()
        self.assertFalse(form2.is_valid())


    def test_passwords_different(self):
        """
        Tests to make sure the form is not valid when the
        password fields do not match.
        """
        self.content['password2'] = 'badpassword'
        form = UserForm(self.content)
        self.assertFalse(form.is_valid())

    def test_username_invalid_symbols(self):
        """
        Tests to make sure users cannot have spaces in their
        username or improper symbols.
        """
        invalid = ['^','[','\w','.','@','+','-',']','+','$']
        for char in invalid:
            self.content['username'] = invalid
            form = UserForm(self.content)
            self.assertFalse(form.is_valid())

    def test_username_invalid_empty(self):
        """
        Tests to make sure users cannot have empty usernames.
        """
        del self.content['username']
        form = UserForm(self.content)
        self.assertFalse(form.is_valid())

    def test_first_name_invalid_empty(self):
        """
        Tests to make sure a users first name cannot be empty.
        """
        del self.content['first_name']
        form1 = UserForm(self.content)
        self.assertFalse(form1.is_valid())

        form2 = EditUserForm(self.content)
        self.assertFalse(form2.is_valid())

    def test_last_name_invalid_empty(self):
        """
        Tests to make sure a users last name cannot be empty.
        """
        del self.content['last_name']
        form1 = UserForm(self.content)
        self.assertFalse(form1.is_valid())

        form2 = EditUserForm(self.content)
        self.assertFalse(form2.is_valid())

    def test_email_invalid_empty(self):
        """
        Tests to make sure a users email cannot be empty.
        """
        del self.content['email']
        form1 = UserForm(self.content)
        self.assertFalse(form1.is_valid())

        form2 = EditUserForm(self.content)
        self.assertFalse(form2.is_valid())

    def test_password1_invalid_empty(self):
        """
        Tests to make sure a users password1 field cannot be empty.
        """
        del self.content['password1']
        form = UserForm(self.content)
        self.assertFalse(form.is_valid())

    def test_password2_invalid_empty(self):
        """
        Tests to make sure a users password2 field cannot be empty.
        """
        del self.content['password2']
        form = UserForm(self.content)
        self.assertFalse(form.is_valid())

    def test_password_invalid_both_empty(self):
        """
        Tests to make sure that if password1=password2=""
        then the form is not valid.
        """
        self.content["password1"] = ""
        self.content["password2"] = ""
        form = UserForm(self.content)
        self.assertFalse(form.is_valid())
