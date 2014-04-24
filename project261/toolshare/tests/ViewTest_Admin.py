"""
File:       toolshare/ViewTest_Admin.py
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

class AdminViewTests(TestCase):
	"""
	A test to test that Admins can admin on the Admin page.
	"""

	def setUp(self):
		"""
		Initialize an admin and non-admin user for the client
		to log in and out of.
		"""
		self.client = Client()
		self.password = "password"

		#get the response for not logged in user
		self.anon_response = self.client.get(reverse('toolshare:admin'))

		#get response for unauthorized user
		self.user = create_live_user(password=self.password)
		self.client.login(username=self.user.username, password=self.password)
		self.unauth_response = self.client.get(reverse('toolshare:admin'))
		self.client.logout()
		
		#get response for authorized user
		self.admin = create_live_user(password=self.password, is_superuser=True)
		self.client.login(username=self.admin.username, password=self.password)
		self.auth_response = self.client.get(reverse('toolshare:admin'))

	def test_status_code(self):
		"""
		test to make sure the status code for the page is 200.
		"""
		self.assertEqual(self.anon_response.status_code, 302)
		self.assertEqual(self.unauth_response.status_code, 404)
		self.assertEqual(self.auth_response.status_code, 200)

	def test_user_list(self):
		"""
		Tests to make sure the list of users is present for the admin.
		"""
		self.assertContains(self.auth_response, "Users")

	def test_sharezone_list(self):
		"""
		Tests to make sure the sharezone list is present.
		"""
		self.assertContains(self.auth_response, "Sharezones")
