from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.http import Http404
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from bs4 import BeautifulSoup
import sherdog
import json
from datetime import datetime


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


def beautiful_soup(request, fighter):
	

	def json_serial(obj):
		if isinstance (obj, datetime):
			serial = obj.isoformat()
        	return serial

	if(fighter == "ronda"):
		scraper = sherdog.Scraper("test")
		#history = scraper.scrape_fighter("Ronda-Rousey", 73073)
		#history = scraper.scrape_fighter("Luke-Rockhold", 23345)
		history = scraper.scrape_fighter("Lyoto-Machida", 7513)

   		title_name = history['name']
		json1 = json.dumps(history)
		#print json1 
		context = {'history':json1, 'title_name':title_name}
		#context = {'history':history}
		return render(request, 'ufc/results.html', context)
	else:
		raise Http404

	