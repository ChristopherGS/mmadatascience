from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.http import Http404
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render


from .models import Fighter, SearchResult


def index(request):
	if request.method == 'POST':
		return render(request, 'ufc/index.html', {'new_item_text':request.POST['item_text']})

	fighter_list = Fighter.objects.all()
	context = {'fighter_list':fighter_list}
	return render(request, 'ufc/index.html', context)


def results(request):
	search_results = SearchResult.objects.all()
	context = {'search_results':search_results}
	return render(request, 'ufc/results.html', context)


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