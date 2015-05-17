import django
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(StaticLiveServerTestCase):

	def setUp(self):
		print self.live_server_url
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)
		

	def tearDown(self):
		pass
		self.browser.quit()