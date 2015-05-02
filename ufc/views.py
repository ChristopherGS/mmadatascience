from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.http import Http404
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from bs4 import BeautifulSoup
import sherdog
import json
from datetime import datetime
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt

import urllib2
import requests
import html5lib


from .models import Fighter, SearchResult


def index(request):
	if request.method == 'POST':
		full_name = request.POST['firstName'] +" "+request.POST['surname']
		Fighter.objects.create(fighter_name=full_name)
		
		return redirect('/searches/all-searches')

	fighter_list = Fighter.objects.all()
	context = {'fighter_list':fighter_list}
	#beautiful_soup()
	return render(request, 'ufc/index.html', context)


def results(request):
	if request.method == 'POST':
		full_name = request.POST['firstName'] +" "+request.POST['surname']
		Fighter.objects.create(fighter_name=full_name)
		context = {'fighter_name':full_name}

		return redirect('/')

	fighter_list = Fighter.objects.all()
	context = {'fighter_list':fighter_list}
	#beautiful_soup()
	return render(request, 'ufc/index.html', context)

def view_list(request):
	#fighter_list = Fighter.objects.all()
	#context = {'fighter_list':fighter_list}
	#beautiful_soup()
	return render(request, 'ufc/results.html')
		

def new_search(request):
	if request.method == 'POST':
		print "new_search method"
		full_name = request.POST['firstName'] +" "+request.POST['surname']
		name = Fighter.objects.create(fighter_name=full_name)
		name.save()
		context = {'fighter_name':name}

		return redirect('/soup/')

def search(request):
	print "search"
	print request.body
	try:
		# should trigger the scraper
		SearchResult(search_data = request.POST['surname']).save()
	except e:
		raise Http404

	finally:
		return HttpResponseRedirect('results')

def scraper(query_first_name, query_surname):
	return "scraper starting for %s" % query_first_name

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

		deeper = fightfinder_result.find_all('tr')

		#AIR PAIR QUESTION 2: clarify when to use "self" - presume not in these functions?

		def extract_link(cell):
			print "THE RAW: ", cell
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
			print "THE RAW: ", cell
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
			print "THE RAW: ", cell
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


		#print "CONTENT", search_results

	#json1 = json.dumps(search_results['bunch'])
	context = {'links':search_results['bunch']}

	print "YO", type(search_results['bunch'])

	#AIRPAIR QUESTION 3: This seems crap - shouldn't I do a redirect here? AND why doesnt the context work easily
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

		
   	title_name = history['fighter_name']
	json1 = json.dumps(history) 
	context = {'history':json1, 'title_name':title_name}
	#context = {'history':json1}
	return render(request, 'ufc/results.html', context)
		

	