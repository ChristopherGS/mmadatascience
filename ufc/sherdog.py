import urllib2
import requests
import html5lib
from datetime import datetime
import json

from bs4 import BeautifulSoup

"""
TODO:

1) create figher search function
2) make bubbles "clickable"
3) create fighter comparison function
4) save top fighters to DB in case of HTML structure change
5) attempt to save significant roster of fighters to DB - automated
6) make bubbles zoomable?
7) alternative visualizations

"""



SHERDOG_URL = 'http://www.sherdog.com'

class Scraper(object):
	"""docstring for Sherdog"""
	def __init__(self, arg):
		super(Scraper, self).__init__()
		self.arg = arg
		self.base_url = SHERDOG_URL


	def scrape_fighter(self, name, fighter_id):

		"""Retrieve and parse a fighter's details from sherdog.com"""
		# make sure fighter_id is an int
		name = str(name)
		fighter_id = str(fighter_id)
		base_url = str(self.base_url)

		# fetch the required url and capture the fighter data
		history = self.process_fighter('/fighter/%s-%s' % (name, fighter_id))

		#print 'scrape fighter data', history
		return history


	def process_fighter(self, url):

		"""Fetch a url and return its contents as a string"""
		
		updated_url = str(self.base_url) + url
		print "here is the url: %s" % updated_url

		source = urllib2.urlopen(updated_url).read()
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
			    birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
			    birth_date = birth_date.isoformat()

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
		last_fight = datetime.strptime(last_fight, '%b / %d / %Y')
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
			conflicts = ["Jungle"]

			for x in conflicts:
				edge_case = eventString.find(x)
				if (edge_case != -1):
					return "*No date   " #hack

			for x in dateStrings: #loop through date strings
				# attempt to find one of the list items in the function argument
				index = eventString.find(x) 

				if (index == -1):
					pass
				else:
					date_string = eventString[index:]
					date_string = date_string.replace(" / ", "-")
					date_string = date_string

					actual_date = datetime.strptime(date_string, '%b-%d-%Y')
					json_date = json.dumps(actual_date, default=json_serial)

					return json_date

		def json_serial(obj):
			if isinstance (obj, datetime):
				serial = obj.isoformat()
        		return serial

		def get_general_method(eventString):
				index = eventString.find('(')
				if (index == -1):
					pass
				else:
					general_method = eventString[:index].rstrip()
					return general_method

		def get_specific_method(eventString):
			index = eventString.find('(')
			end_index = eventString.find(')')
			if (index == -1):
				pass
			else:
				specific_method = eventString[index+1:end_index].rstrip()
				return specific_method

		def get_ref(eventString):
			index = eventString.find(')')
			if (index == -1):
				pass
			else:
				return eventString[index+1:]

		def get_sec(s):
			convert_to_string = str(s)
			l = convert_to_string.split(':')
			return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])


		def get_total_time(time, tround):
			
			try:
				around = int(tround)
				the_round = around 

				the_time = datetime.strptime(time, '%M:%S').time()
				the_time = get_sec(the_time)
				
				total_fight_time = 0


				print "TIME:", the_time
				#print type(the_time)

				if the_round == 1:
					total_fight_time = the_time
				elif the_round == 2:
					total_fight_time = the_time + (5*60)
				elif the_round == 3:
					total_fight_time = the_time + (10*60)
				elif the_round == 4:
					total_fight_time = the_time + (15*60)
				elif the_round == 5:
					total_fight_time = the_time + (20*60)

				return total_fight_time

			except Exception as e:
				print "Exception:", e



		records = {}
		records = soup.findAll('table')[0].findAll('tr')
		
		d3 = {}
		d3['name'] = result['name']
		d3['value'] = 100 #should be total career fight time in seconds TODO
		d3['total_fight_time'] = ""
		d3['children'] = []
		content = []
		
		for row in records:
			cells = row.find_all('td')

			print "HTML:", cells

			content = {

				"opponent": cells[1].get_text(),
				"win_loss": cells[0].get_text(),
				"_event": getEvent(cells[2].get_text()),
				"date": getDate(cells[2].get_text()),
				"method_general": get_general_method(cells[3].get_text()),
				"method_specific": get_specific_method(cells[3].get_text()),
				"referee": get_ref(cells[3].get_text()),
				"_round": cells[4].get_text(),
				"round_time": cells[5].get_text(),
				"total_time": get_total_time(cells[5].get_text(), cells[4].get_text()),
				"value": get_total_time(cells[5].get_text(), cells[4].get_text())
				#"value": 25 #required for D3 graphing TODO: use time value in seconds
			}



			d3['children'].append(content)
			
		#print "D3 DATA (pre-cleanup):", d3


		def clean_up(history):
			#remove the first entry as these are just row titles
			d3['children'].pop(0) 

		clean_up(d3)


		#now let's create the total career time

		def calc_career_time():
			career_time = 0
			for duration in d3['children']:
				for key, value in duration.iteritems():
					if key == "total_time":
						#print value
						career_time += value
			print "career_time:", career_time
			d3['total_fight_time'] = career_time
			d3['value'] = career_time


		calc_career_time()

		#print "D3 DATA (POST-cleanup):", d3

		return d3
	


if __name__ == "__main__":
	pass