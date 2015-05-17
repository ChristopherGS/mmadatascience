from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.test import Client, TestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from ufc.views import index

from .models import Fighter, SearchResult


class WebTests(TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()
