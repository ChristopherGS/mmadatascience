from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.http import Http404
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from bs4 import BeautifulSoup
import sherdog


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


def beautiful_soup(request):
	
	print sherdog.SHERDOG_URL

	scraper = sherdog.Scraper("test")

	scraper.crawl("Anderson Silva")

	#print soup.prettify()
	#print soup.title
	#print soup.title.string
	#print soup.get_text()

	#for link in soup.find_all('a'):
	#	print(link.get('href'))

	#soup.find_all(text="Elsie")
	#A tag's children are available in a list called .contents:
	return render(request, 'ufc/results.html')