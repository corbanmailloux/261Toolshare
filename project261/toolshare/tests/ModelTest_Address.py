"""
File:       toolshare/tests/ModelTest_Address.py
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

class AddressTests(TestCase):
    """
    Tests the functionality of the address class
    """

    def setUp(self):
        """
        Sets up addresses for the testing of functions within the Address classbject):
        """
        line1_1 = "42 Testers Avenue"
        line2_1 = "Appartment # 9 3/4"
        line1_2 = "45 Test Street"
        line2_2 = "Appartment 3"
        zipcode = "12345"
        zipcode2 = "54321"
        self.address1 = Address.objects.create(line1=line1_1,line2=line2_1,zip=zipcode)
        self.address2 = Address.objects.create(line1=line1_2,line2=line2_2,zip=zipcode)
        #address 3 is in a different zipcode
        self.address3 = Address.objects.create(line1=line1_2,line2=line2_2,zip=zipcode2)


    def test_zip_is_integer(self):
        """
        Tests to make sure the zip_is_integer function correctly determines that
        the zipcode is a positive integer and not a negative number, or contains
        non-numerical characters.
        """
        self.assertTrue(Address.zip_is_integer("12345"))
        self.assertFalse(Address.zip_is_integer("abcde"))
        self.assertFalse(Address.zip_is_integer("-12345"))

