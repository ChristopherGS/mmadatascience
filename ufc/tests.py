from django.test import TestCase

from django.core.urlresolvers import reverse

from selenium import webdriver

from .models import Fighter, SearchResult


class WebTests(TestCase):
	def test_check_browser(self):
		browser = webdriver.Firefox()
		browser.get('http://localhost:8000')

		assert 'Django' in browser.title


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
