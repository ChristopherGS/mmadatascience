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

	def test_check_browser(self):

		self.browser.get('http://localhost:8000')
		#self.assertIn('localhost', self.browser.title)

"""
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
		request.POST['firstName'] = 'Jon'
		request.POST['surname'] = 'Jones'

		response = index(request)

		self.assertEqual(Fighter.objects.count(), 1)
		new_fighter = Fighter.objects.first()
		self.assertEqual(new_fighter.fighter_name, 'Jon Jones')

	def test_home_page_redirects_after_POST(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['firstName'] = 'Jon'
		request.POST['surname'] = 'Jones'

		response = index(request)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], '/')
"""
"""
no longer needed due to redirect
		self.assertIn('Jon Jones', response.content.decode())
		expected_html = render_to_string(
			'ufc/index.html',
			{'search_text':  'Jon Jones'}
		)
		self.assertEqual(response.content.decode(), expected_html)
"""
#Beautiful soup should be available from index.html
"""
def create_search_result(search_data):
"""
"""
Creates a question with the given `question_text` published the given
number of `days` offset to now (negative for questions published
in the past, positive for questions that have yet to be published).
"""
"""
	return SearchResult.objects.create(search_data = search_data)
"""
"""
class FighterModelTest(TestCase):
	def test_saving_and_retrieving_fighters(self):
		first_fighter = Fighter()
		first_fighter.fighter_name = 'The first fighter'
		first_fighter.save()

		second_fighter = Fighter()
		second_fighter.fighter_name = 'Fighter the second'
		second_fighter.save()

		saved_fighters = Fighter.objects.all()
		self.assertEqual(saved_fighters.count(), 2)
		
		first_saved_fighter = saved_fighters[0]
		second_saved_fighter = saved_fighters[1]
		self.assertEqual(first_saved_fighter.fighter_name, 'The first fighter')
		self.assertEqual(second_saved_fighter.fighter_name, 'Fighter the second')
"""

class ListViewTest(TestCase):

	def test_displays_all_items(self):
		Fighter.objects.create(fighter_name='Chael Sonnen')
		Fighter.objects.create(fighter_name='Vitor Belfort')
		"""Instead of calling the view function directly, we use the Django test client, 
		which is an attribute of the Django TestCase called  self.client. 
		"""
		response = self.client.get('/searches/all-searches/') #1

		"""
		Instead of using the slightly annoying  assertIn/response.content.decode() dance, Django provides the  
		assertContains method which knows how to deal with responses and the bytes of their content."""
		self.assertContains(response, 'Chael Sonnen') #2
		self.assertContains(response, 'Vitor Belfort') #3

	def test_uses_results_template(self):
		response = self.client.get('/ufc/searches/all-searches/')
		self.assertTemplateUsed(response, 'ufc/results.html')



class ListComprehensionPractice(TestCase):
	
	def test_basic(self):
		evenIntegers = [x for x in range(11) if x%2 == 0]
		self.assertEqual(evenIntegers[1], 2)
		self.assertEqual(len(evenIntegers), 6)

	def test_moderate(self):
		even_divisible_by_five = [x for x in range(11) if x%2 == 0 and x%5 == 0]
		self.assertEqual(even_divisible_by_five[1],10)

	def test_hard(self):
		fibinacci = [(x.upper(), y) for x in ["yo", "hey", "waddup"] for y in [1,2,3]]
		#notice how because the x is the first for loop, each of its elements in multiplied
		#first - like matrix mulitplication
		self.assertEqual(fibinacci[2], ("YO", 3))
		print fibinacci

	def test_very_hard(self):
		sentence = "how many toes does a fish have"
		page = []
		
		page = [word for word in sentence.split()]
		print page

		blah = [(x,y) for x in ["toes","wings"] for y in [10, 2]]
		print blah

class NewListTest(TestCase):

	def test_saving_a_POST_request(self):
		self.client.post(
		    '/ufc/searches/new/',
		    data={'firstName': 'Lyoto', 'surname': 'Machida'}
		)
		self.assertEqual(Fighter.objects.count(), 1)
		new_fighter = Fighter.objects.first()
		self.assertEqual(new_fighter.fighter_name, 'Lyoto Machida')

	def test_redirects_after_POST(self):
		response = self.client.post(
		    '/ufc/searches/new',
		    data={'firstName': 'Lyoto', 'surname': 'Machida'}
		)
		self.assertEqual(response.status_code, 301)

	def test_redirects_after_POST(self):
		response = self.client.post(
		    '/ufc/searches/new',
		    data={'firstName': 'Lyoto', 'surname': 'Machida'}
		)
		self.assertRedirects(response, '/ufc/soup/')


class BeautifulSoupTests(TestCase):

	def test_simple(self):
		x = 'yo'
		self.assertEqual('foo'.upper(), 'FOO' )

	def test_query_return_value(self):
		pass
		#create_search_result(search_data="Dummy search result")
		#response = self.client.get(reverse('ufc:index'))
		#self.assertEqual(response.status_code, 200)
"""
A POST to the 'search' route should trigger a search query with Beautiful Soup
and return a value
"""
