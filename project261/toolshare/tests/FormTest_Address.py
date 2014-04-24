from django.test import TestCase
from ..forms import AddressForm

class UserRegistrationTest(TestCase):
    """
    This will test the AddressForm. 
    It will most extensivly check zipcodes. line1 and line2 
    will be touched upon as well but as these are just strings there is
    not much to varify.
    """

    def setUp(self):
        """
        Initializes default form data for Address and initializes the test
        Client.
        """
        self.content = {
            'line1':'test',
            'line2':'test',
            'zip': '12345',
            }

    def test_standard_valid(self):
        """
        Tests to make sure the standard input with a valid line1, 
        line2, and zip code is valid in the form.
        """
        form = AddressForm(self.content)
        self.assertTrue(form.is_valid())

    def test_zip_edge1(self):
        """
        Tests to make sure the edge case where the zip code is 
        00000 is valid.
        """
        self.content['zip'] = '00000'
        form = AddressForm(self.content)
        self.assertTrue(form.is_valid())

    def test_zip_edge2(self):
        """
        Tests to make sure the edge case 99999 is valid.
        """
        self.content['zip'] = '99999'
        form = AddressForm(self.content)
        self.assertTrue(form.is_valid())

    def test_zip_negative(self):
        """
        Ensures the zip code cannot have a negative value
        Note: the max length is 5 so I want to make sure it
        fails not just because there's technically 6 characters.
        So I am testing for '-11111' and '-1111'
        """
        self.content['zip'] = '-11111'
        form = AddressForm(self.content)
        self.assertFalse(form.is_valid())

        self.content['zip'] = '-1111'
        form = AddressForm(self.content)
        self.assertFalse(form.is_valid())

    def test_zip_too_short(self):
        """
        Checks to make sure zip codes that are too short are not valid.
        """
        self.content['zip'] = '1111'
        form = AddressForm(self.content)
        self.assertFalse(form.is_valid())

    def test_zip_too_long(self):
        """
        Tests to make sure a zip code cannot be too long.
        """
        self.content['zip'] = '111111'
        form = AddressForm(self.content)
        self.assertFalse(form.is_valid())

    def test_zip_empty(self):
        """
        Makes sure the zip code may not be empty.
        """
        del self.content['zip'] #deletes zip from dict
        form = AddressForm(self.content)
        self.assertFalse(form.is_valid())

    def test_line1_empty(self):
        """
        Tests to make sure line 1 may not be empty.
        """
        del self.content['line1'] #deletes line1 from dict
        form = AddressForm(self.content)
        self.assertFalse(form.is_valid())

    def test_line2_empty(self):
        """
        Tests to make sure line 2 MAY be empty.
        """
        del self.content['line2'] #deletes line1 from dict
        form = AddressForm(self.content)
        self.assertTrue(form.is_valid())

    def test_all_empty(self):
        """
        Tests to make sure the whole shebang cannot be empty.
        """
        form = AddressForm()
        self.assertFalse(form.is_valid())
