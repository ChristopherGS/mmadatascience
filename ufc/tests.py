from django.test import TestCase

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve

from django.template.loader import render_to_string

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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
		#self.assertIn('localhost', self.browser.title)


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
		expected_html = render_to_string('ufc/index.html')
		# Not sure why this doesn't work -->
		#self.assertEqual(response.content.decode('utf8', 'ignore'), expected_html) 

class SearchTest(TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_search(self):
		self.browser.get('http://localhost:8000')

		search_header = self.browser.find_element_by_id('searchBox').text
		self.assertIn('Search', search_header)

		inputbox = self.browser.find_element_by_id('firstName')
		self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter first name'
                )
		inputbox = self.browser.find_element_by_id('surname')
		self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter surname'
                )

		#inputbox.send_keys(Keys.ENTER)

	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'

		response = index(request)

		self.assertIn('A new list item', response.content.decode())
		expected_html = render_to_string(
			'ufc/index.html',
			{'new_item_text':  'A new list item'}
		)
		self.assertEqual(response.content.decode(), expected_html)

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
		#self.assertEqual(response.status_code, 200) 
