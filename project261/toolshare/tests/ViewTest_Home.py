"""
File:       toolshare/ViewTest_Home.py
Language:   Python 3 with Django Web Framework

Author:     Val Booth <vxb4825@rit.edu>
Author:     Corban Mailloux <cdm3806@rit.edu>
Author:     Adam McCarthy <aem1269@rit.edu>
Author:     Michael Washburn <mdw7326@rit.edu>
Author:     Bryon Wilkins <brw4824@rit.edu>


"""

from django.test import TestCase
from .testutils import *
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test.client import RequestFactory
from django.contrib.auth import views

class HomeViewTests_logged_out(TestCase):
    """
    Tests to make sure the Home page displays the proper information.
    """
    def setUp(self):
        """
        Initialize the test client and
        url for the home page.
        """
        self.client = Client()
        self.url = reverse('toolshare:home')
        self.response = self.client.get(self.url)

    def test_status(self):
        """
        Tests to make sure the page loads with the proper 
        status code for unauthenticated users.
        """
        self.assertEqual(self.response.status_code, 200)

    def test_is_guest(self):
        """
        Tests to make sure "Guest" is displayed on the page as the user.
        """
        self.assertContains(self.response, "Guest")

    def test_basic_statistics(self):
        """
        Tests to make sure the basic_statistics section
        is shown in the home page. for an unauthenticated user.
        """
        self.assertContains(self.response, "Basic Statistics")

    def test_average_tool_quality(self):
        """
        Tests to make sure the Average Tool quality stats are shown.
        """
        self.assertContains(self.response, "Average Tool Quality")

    def test_most_popular_sharezones(self):
        """
        Tests to make sure the sharezone Statistics are not available
        to logged out users.
        """
        self.assertNotContains(self.response, "Most Popular Sharezones")




class HomeViewTests_logged_in(TestCase):
    """
    Tests the home view for logged in users.
    """

    def setUp(self):
        """
        Initializes the test client and logs it in.
        """
        #initialize a live user, then log in.
        self.password = "password"
        self.user = create_live_user(password=self.password)
        self.logged_in = self.client.login(username=self.user.username, password=self.password)

        #gets the home page as a signed in user.
        #response contains the source of the page
        self.response = self.client.get(reverse('toolshare:home'))

    def test_status(self):
        """
        Tests to make sure the page loads with the proper 
        status code for authenticated users.
        """
        self.assertEqual(self.response.status_code, 200)

    def test_username_displayed(self):
        """
        Test to make sure the current user's username is displayed
        on the page (In the top right corner is where it is.)
        """
        self.assertContains(self.response, self.user.username)

    def test_first_name_displayed(self):
        """
        Tests to make sure that the first name of the user is displayed.
        It should be within the welcome message.
        """
        self.assertContains(self.response, self.user.first_name)

    def test_basic_statistics(self):
        """
        Tests to make sure the basic_statistics section
        is shown in the home page. for an authenticated user.
        """
        self.assertContains(self.response, "Basic Statistics")

    def test_average_tool_quality(self):
        """
        Tests to make sure the Average Tool quality stats are shown.
        """
        self.assertContains(self.response, "Average Tool Quality")

    def test_most_popular_sharezones(self):
        """
        Tests to make sure the sharezone Statistics are available
        to logged in users.
        """
        self.assertContains(self.response, "Most Popular Sharezones")
        