import urllib2
import requests
import mechanize
import html5lib
import datetime

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

		#print soup.body
		fighter_name = soup.find_all("span", class_="fn")
		fighter_namey = soup.find('h1', {'itemprop': 'name'}).span.contents[0]
		print fighter_name

		print fighter_namey


		try:
			birth_date = soup.find('span', {'itemprop': 'birthDate'}).contents[0]
		except AttributeError:
			birth_date = None
		else:
			if birth_date == 'N/A':
			    birth_date = None
			else:
			    birth_date = datetime.datetime.strptime(birth_date, '%Y-%m-%d')
			    birth_date = birth_date.isoformat()

		print 'birthday', birth_date


			# get the fighter's locality
		try:
			locality = soup.find('span', {'itemprop': 'addressLocality'}).contents[0]
		except AttributeError:
			locality = None

			# get the fighter's locality
		try:
			nationality = soup.find('strong', {'itemprop': 'nationality'}).contents[0]
		except AttributeError:
			nationality = None

			# get the fighter's height in CM
		try:
			height_cm = soup.find('span', {'class': 'item height'}).contents[-1].lstrip().rstrip().replace(' cm', '')
		except AttributeError:
			height_cm = None

			# get the fighter's weight in KG
		try:
			weight_kg = soup.find('span', {'class': 'item weight'}).contents[-1].lstrip().rstrip().replace(' kg', '')
		except AttributeError:
			weight_kg = None

			# get the fighter's camp/team
		try:
			camp_team = soup.find('h5', {'class': 'item association'}).strong.span.a.span.contents[0]
		except AttributeError:
			camp_team = None

		wld = {}
		wld['wins'] = 0
		wld['losses'] = 0
		wld['draws'] = 0
		wlds = soup.findAll('span', {'class': 'result'})
		for x in wlds:
			wld[x.contents[0].lower()] = x.findNextSibling('span').contents[0]

		last_fight = soup.find('span', {'class': 'sub_line'}).contents[0]
		last_fight = datetime.datetime.strptime(last_fight, '%b / %d / %Y')
		last_fight = last_fight.isoformat()

			# build a dict with the scraped data and return it
		result = {
			'name': fighter_namey,
			'birth_date': birth_date,
			'locality': locality,
			'nationality': nationality,
			'height_cm': height_cm,
			'weight_kg': weight_kg,
			'camp_team': camp_team,
			#'id': fighter_id,
			'wins': wld['wins'],
			'losses': wld['losses'],
			'draws': wld['draws'],
			'last_fight': last_fight,
			}


		record = soup.find('span', {'class': 'final_result'}).contents[0]
		# the record table is the second table on the page
		
		records = {}
		records = soup.findAll('table')[1].findAll('tr')

		#for td in soup.select('table(1) > tr > td:nth-of-type(1)'):

		history = {}
		history['win_loss'] = []
		history['opponent'] = []
		history['event'] = []
		history['date'] = []
		history['method_general'] = []
		history['method_specific'] = []
		history['referee'] = []
		history['_round'] = []
		history['time'] = []

		def getEvent(eventString):
			dateStrings = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
			for x in dateStrings:
				index = eventString.find(x)
				if (index == -1):
					pass
				else:
					return eventString[:index]

		def getDate(eventString):
			dateStrings = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
			for x in dateStrings:
				index = eventString.find(x)
				if (index == -1):
					pass
				else:
					return eventString[index:]

		def get_general_method(eventString):
				index = eventString.find('(')
				if (index == -1):
					pass
				else:
					return eventString[:index]

		def get_specific_method(eventString):
			index = eventString.find('(')
			end_index = eventString.find(')')
			if (index == -1):
				pass
			else:
				return eventString[index+1:end_index]

		def get_ref(eventString):
			index = eventString.find(')')
			if (index == -1):
				pass
			else:
				return eventString[index+1:]


		for row in records:
			cells = row.find_all('td')
			win_loss = [cells[0].get_text()] 
			opponent = cells[1].get_text()
			event = getEvent(cells[2].get_text())
			date = getDate(cells[2].get_text()) #print event #need to work magic here to separate date
			method_general = get_general_method(cells[3].get_text())
			method_specific = get_specific_method(cells[3].get_text())
			referee = get_ref(cells[3].get_text())
			_round = cells[4].get_text()
			time = cells[5].get_text()

			history['win_loss'].append(win_loss)
			history['opponent'].append(opponent)
			history['event'].append(event)
			history['date'].append(date) 
			history['method_general'].append(method_general)
			history['method_specific'].append(method_specific)
			history['referee'].append(referee)
			history['_round'].append(_round)
			history['time'].append(time)

		
		print history

		print result

		return #result.text

	def scrape_fighter(self, name, fighter_id):

		"""Retrieve and parse a fighter's details from sherdog.com"""
		# make sure fighter_id is an int
		name = str(name)
		fighter_id = str(fighter_id)
		base_url = str(self.base_url)

		# fetch the required url and parse it
		url_content = self.fetch_url('/fighter/%s-%s' % (name, fighter_id))


if __name__ == "__main__":
	pass