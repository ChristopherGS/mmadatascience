import json
import urllib2
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from django.forms.models import model_to_dict
from django.http import (Http404, HttpRequest, HttpResponse,
                         HttpResponseRedirect, JsonResponse)
from django.shortcuts import get_object_or_404, redirect, render
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt

import sherdog

from .models import Fighter, SearchResult


def index(request):
	fighter_list = Fighter.objects.all()
	context = {'fighter_list':fighter_list}
	return render(request, 'ufc/index.html', context)


def view_list(request):
	return render(request, 'ufc/results.html')
		

def scraper(query_first_name, query_surname):
	return "scraper starting for %s" % query_first_name



# AIRPAIR QUESTION 4: How can I easily "pass stuff around" like I tried to do here?
# Ended up doing all the url wrangling on the client
@csrf_exempt
def organize(request):
	if request.method == 'POST':
		whole_url = str(request.POST['o_url'])
		print "FULL URL: ", whole_url
		try:
			edited = whole_url.strip('http://www.sherdog.com/fighter/')
			sherdog_id = str(''.join([i for i in edited if i.isdigit()]))
			fighter_name = str(''.join([i for i in edited if not i.isdigit()]))
		except Exception as e:
			print e

		print fighter_name[0]
		print sherdog_id
		info = {'fighter_name': fighter_name, 'sherdog_id': sherdog_id}
		json = json.dumps(info)
		#return redirect('/ufc/soup/%s/%s' % (fighter_name, sherdog_id))
		return JsonResponse(info)


@csrf_exempt
def hunt(request):

	if request.method == 'POST':
		full_name = request.POST['surname'] +"+"+request.POST['firstName']
		print "FULL NAME POST: ", full_name
		
		scraper = sherdog.Scraper("test")
		SHERDOG_URL = 'http://www.sherdog.com/stats/fightfinder'
		#http://www.sherdog.com/stats/fightfinder?SearchTxt=Aldo&weight=&association=
		search = str(full_name)
		search = search.strip(" ")
		url = "?SearchTxt=%s&weight=&association=" % search

		complete_url = str(SHERDOG_URL) + url
		print "here is the search url: %s" % complete_url

		source = urllib2.urlopen(complete_url).read()
		soup = BeautifulSoup(source)

		fightfinder_result = soup.find("table", { "class" : "fightfinder_result" })

		#MANAGE THE EVENT OF NOT FINDING ANYTHING
		try: 
			deeper = fightfinder_result.find_all('tr')
		except Exception as e:
			print "NO SEARCH RESULtS", e
			context = {'error':'No search results found'}
			return render(request, 'ufc/search.html', context)


		#AIR PAIR QUESTION 2: clarify when to use "self" - presume not in these functions?

		def extract_link(cell):
			anchors = cell.find_all('a')
			try:
				for a in anchors:
					edited = a['href'].strip('/fighter/')
					result = ''.join([i for i in edited if not i.isdigit()])
					result = result.rstrip('-')
					print "edited", result
					return result
			except:
				print "NO!"
				return "NA"

		def extract_sherdog(cell):
			anchors = cell.find_all('a')
			try:
				for a in anchors:
					test = str(a['href'])
					edited = ''.join([i for i in test if i.isdigit()]) # the part to omit
					print edited
					return edited
			except:
				print "NO!"
				return "NA"

		def extract_image(cell):
			images = cell.find_all('img')
			try:
				for i in images:
					return i['src']
			except:
				print "NO!"
				return "NA"


		search_results = {}
		search_results['bunch'] = []

		for row in deeper:
			cells = row.find_all('td')
			
			try:
				content = {
					"result_name": cells[1].get_text(),
					"result_url": extract_link(cells[1]),
					"result_sherdog_id": extract_sherdog(cells[1]),
					"result_image": extract_image(cells[0]),
				}
				
			except Exception as e:
				print "EXCEPTIoN", e
				content = {}
			finally:
				search_results['bunch'].append(content)


	#del the first result as that is the table headings
	del search_results['bunch'][0]

	context = {'links':search_results['bunch']}

	#AIRPAIR QUESTION 3: This seems crap - shouldn't I do a redirect here? AND why doesnt the context work easily
	# feel like I'm forced to rebuild the html, rather than letting another view handle it
	return render(request, 'ufc/search.html', context)
		


def beautiful_soup(request, fighter, sherdog_id):
	print type(fighter)
	print type(sherdog_id)

	def json_serial(obj):
		if isinstance (obj, datetime):
			serial = obj.isoformat()
        	return serial

	scraper = sherdog.Scraper("test")

	try:	
		history = scraper.scrape_fighter(fighter, sherdog_id)
	except Exception as e:
		print e
		raise Http404

	print history
   	title_name = history['fighter_name']
   	image_url = history['image_url']
	json1 = json.dumps(history) 
	context = {'history':json1, 'title_name':title_name, 'image_url': image_url}
	#context = {'history':json1}
	return render(request, 'ufc/results.html', context)
