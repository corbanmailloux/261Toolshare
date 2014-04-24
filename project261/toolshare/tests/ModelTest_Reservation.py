"""
File:       toolshare/tests/ModelTest_Reservation.py
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
from django.utils import timezone
import datetime
from .testutils import *

class ReservationTests(TestCase):
    """
    Tests the functionality of the Reservation class.
    """
    # TODO: valid reservations are valid
    # TODO: reservations for unshared tools are invalid
    # TODO: reservation with conflicting reservations is invalid
    # TODO: reservation in the past is invalid
    # TODO: reservation for unshared tool is invalid

    def setUp(self):
        group = ToolGroup.objects.create(name="Test Tools 1")
        self.user_list = [User.objects.create(username=("user%d" % i), password="pass") for i in range(0, 10)]
        sharezone = create_sharezone()
        self.tool_list = [Tool.objects.create(owner=self.user_list[i], renter=None,
            name=("Tool%d" % i), group=group, sharezone=sharezone, shared=True,
            description="", instructions="") for i in range(0, 10)]
        self.now = timezone.now()

    def test_single_reservation_is_valid(self):
        """
        The reservation validators should all return True for a non-conflicting
        reservation of 14 days.
        """
        user_list, tool_list = self.user_list, self.tool_list
        res = Reservation.objects.create(tool=tool_list[0], user=user_list[0], start_date=self.now,
            end_date = self.now + datetime.timedelta(days=14))
        self.assertTrue(res.is_not_conflicting())
        self.assertTrue(res.is_valid_length())
        self.assertTrue(res.is_valid())
        self.assertFalse(Reservation.objects.all().count() == 0) #res added to DB

    def test_single_reservation_invalid_length(self):
        """
        The reservation length validator should return False since the length
        is 15 days, but the conflict validator should return True since there
        are no conflicts. The general validator should return False.
        """
        user_list, tool_list = self.user_list, self.tool_list
        res = Reservation.objects.create(tool=tool_list[1], user=user_list[1],
            start_date=self.now, end_date=(self.now + datetime.timedelta(days=15)))
        self.assertTrue(res.is_not_conflicting())
        self.assertFalse(res.is_valid_length())
        self.assertFalse(res.is_valid())

    def test_backwards_reservation(self):
        """
        The reservation length validator should catch the case when the end
        date is before the start date.
        """
        user_list, tool_list = self.user_list, self.tool_list
        res = Reservation.objects.create(tool=tool_list[2], user=user_list[2],
            start_date=self.now + datetime.timedelta(days=1), end_date = self.now)
        self.assertTrue(res.is_not_conflicting())
        self.assertFalse(res.is_valid_length())
        self.assertFalse(res.is_valid())

    def test_conflicting_reservations(self):
        """
        The reservation length validator should pass for both reservations,
        since they are 14 days or less. However, the conflict validator should
        return False.
        """
        user_list, tool_list = self.user_list, self.tool_list
        res = Reservation.objects.create(tool=tool_list[3], user=user_list[3],
            start_date=self.now, end_date = self.now + datetime.timedelta(days=2))
        self.assertTrue(res.is_valid_length())
        self.assertTrue(res.is_not_conflicting())
        self.assertTrue(res.is_valid())

        res2 = Reservation.objects.create(tool=tool_list[3], user=user_list[0],
            start_date=self.now + datetime.timedelta(days=1),
            end_date=self.now + datetime.timedelta(days=3))
        self.assertTrue(res2.is_valid_length())
        self.assertFalse(res2.is_not_conflicting())
        self.assertFalse(res2.is_valid())