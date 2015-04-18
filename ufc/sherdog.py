import urllib2
import requests
import mechanize
import html5lib

from bs4 import BeautifulSoup

print 'blah'


SHERDOG_URL = 'http://www.sherdog.com'

#result = requests.get(SHERDOG_URL, verify=False)

#print result.status_code

#print result.headers

#s = requests.Session()
#result = s.get(SHERDOG_URL)


#c = result.content




#r = s.get("http://httpbin.org/cookies")
#print(r.text)
# '{"cookies": {"sessioncookie": "123456789"}}'
#s.auth = ('user', 'pass')
#s.headers.update({'x-test': 'true'})

class Scraper(object):
	"""docstring for Sherdog"""
	def __init__(self, arg):
		super(Scraper, self).__init__()
		self.arg = arg
		self.base_url = SHERDOG_URL

		
	def crawl(self, fighter):
		print SHERDOG_URL + 'scrape'

		self.scrape_fighter('Ronda-Rousey', 73073)
		#soup = BeautifulSoup(self.url)
		#print soup.prettify()
		return

	def fetch_url(self, url):

		"""Fetch a url and return it's contents as a string"""
		
		updated_url = str(self.base_url) + url
		print "here is the url: %s" % updated_url

		#s = requests.Session()
		#headers = {'user-agent': 'my-app/0.0.1'}
		#result = s.get('https://www.sherdog.com', headers=headers, timeout=40, verify=False)

		aurl = 'http://www.sherdog.com/fighter/Luke-Rockhold-23345'
		source = urllib2.urlopen(aurl).read()
		soup = BeautifulSoup(source)

		print soup.body
		fighter_name = soup.find_all("span", class_="fn")
		print fighter_name

		#print 'status code', soup.status_code
		#print 'headers', soup.headers
		#print 'cookies', requests.utils.dict_from_cookiejar(s.cookies)
		return #result.text

	def scrape_fighter(self, name, fighter_id):

		"""Retrieve and parse a fighter's details from sherdog.com"""
		# make sure fighter_id is an int
		name = str(name)
		fighter_id = str(fighter_id)
		base_url = str(self.base_url)

		# fetch the required url and parse it
		url_content = self.fetch_url('/fighter/%s-%s' % (name, fighter_id))
		#soup = BeautifulSoup(url_content, 'html5lib')

		#print soup.body

		#fighter_name = soup.find_all("span", class_="fn")

		#print fighter_name



	def search(cls, query):
		pass
#		query = urllib2.quote(query.lower())
#		dom = Sherdog.fetch_and_parse_url(cls._search_url_path % query)
#		table = dom.find('table', {'class': 'fightfinder_result'})
#		urls = [a['href'] for a in table.findAll('a')]
#		return map(cls, filter(_FIGHTER_URL_RE.match, urls))


if __name__ == "__main__":
	pass