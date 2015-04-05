from django.test import TestCase

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve

from selenium import webdriver

from .models import Fighter, SearchResult
from ufc.views import index


class WebTests(TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_check_browser(self):

		self.browser.get('http://localhost:8000')
		self.assertIn('localhost', self.browser.title)


class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, index)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = index(request)
		#self.assertTrue(response.content.startswith(b'<link rel="stylesheet" type="text/css" href="/static/ufc/css/bootstrap.css" />'))
		self.assertIn(b'<h1>Python Scraper for UFC Fighters</h1>', response.content)
		self.assertTrue(response.content.endswith(b'</div>'))





#Beautiful soup should be available from index.html

def create_search_result(search_data):
	"""
	Creates a question with the given `question_text` published the given
	number of `days` offset to now (negative for questions published
	in the past, positive for questions that have yet to be published).
	"""

	return SearchResult.objects.create(search_data = search_data)

class BeautifulSoupTests(TestCase):

	def test_simple(self):
		x = 'yo'
		self.assertEqual('foo'.upper(), 'FOO' )

	def test_query_return_value(self):
		"""
		A POST to the 'search' route should trigger a search query with Beautiful Soup
		and return a value
		"""
		create_search_result(search_data="Dummy search result")
		response = self.client.get(reverse('ufc:index'))
		self.assertEqual(response.status_code, 200) 
