"""
File:       toolshare/FormTest_Reservation.py
Language:   Python 3 with Django Web Framework

Author:     Val Booth <vxb4825@rit.edu>
Author:     Corban Mailloux <cdm3806@rit.edu>
Author:     Adam McCarthy <aem1269@rit.edu>
Author:     Michael Washburn <mdw7326@rit.edu>
Author:     Bryon Wilkins <brw4824@rit.edu>

"""

from django.test import TestCase
from ..forms import ReservationForm
from .testutils import *
from django.utils import timezone
import datetime

class ReservationFormTests(TestCase):
    """
    Tests to make sure the reservation accepts only the allowed input formats.
    """

    def setUp(self):
        """
        Initialize users, tools, and reservatin form data.
        Dates are in the following forms:
        """
        self.start_date = timezone.now()
        self.end_date = timezone.now() + datetime.timedelta(days=1)
        self.instance = create_tool()
        self.content = {
            'start_date' : self.start_date,
            'end_date' : self.end_date,
        }

    def test_standard_valid(self):
        """
        Tests a standard reservation input.
        """
        form = ReservationForm(self.content, instance=self.instance)
        self.assertTrue(form.is_valid())

    def test_all_empty(self):
        """
        Tests to make sure the form is not valid without start or end input.
        """
        form = ReservationForm(instance=self.instance)
        self.assertFalse(form.is_valid())

    def test_start_empty(self):
        """
        Tests to make sure the start date cannot be empty.
        """
        del self.content['start_date']
        form = ReservationForm(self.content, instance=self.instance)
        self.assertFalse(form.is_valid())

    def test_end_empty(self):
        """
        Tests to make sure the end date cannot be empty.
        """
        del self.content['end_date']
        form = ReservationForm(self.content, instance=self.instance)
        self.assertFalse(form.is_valid())

    def test_date_in_past(self):
        """
        Tests to make sure the date cannot be in the past (beyond an hour)
        """
        self.content['start_date'] = timezone.now() - datetime.timedelta(days=1)
        self.content['end_date'] = timezone.now() + datetime.timedelta(days=1)

        form = ReservationForm(self.content, instance=self.instance)
        self.assertFalse(form.is_valid())

    def test_time_too_long_inside_edge(self):
        """
        Tests to make sure that a reservation CAN be up to two weeks long.
        """
        self.content['end_date'] = timezone.now() + datetime.timedelta(days=14)
        self.content['start_date'] = timezone.now()

        form = ReservationForm(self.content, instance=self.instance)
        self.assertTrue(form.is_valid())

    def test_time_too_long_outside_edge(self):
        """
        Tests to make sure that the time cannot be longer than two weeks.
        """
        self.content['end_date'] = timezone.now() + datetime.timedelta(days=15)
        self.content['start_date'] = timezone.now()

        form = ReservationForm(self.content, instance=self.instance)
        self.assertFalse(form.is_valid())

    def test_end_before_start(self):
        """
        Tests to make sure the end date cannot be before the start date.
        """
        self.content['end_date'] = timezone.now()
        self.content['start_date'] = timezone.now() + datetime.timedelta(days=1)

        form = ReservationForm(self.content, instance=self.instance)
        self.assertFalse(form.is_valid())
