import json
import logging
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

logger = logging.getLogger(__name__)


def index(request):
    fighter_list = Fighter.objects.all()
    context = {'fighter_list':fighter_list}
    return render(request, 'ufc/index.html', context)


def retrieve_results(full_name):
    """get the data from a fighter search"""

    SHERDOG_URL = 'http://www.sherdog.com/stats/fightfinder'
    search = str(full_name)
    search = search.strip(" ")
    url = "?SearchTxt=%s&weight=&association=" % search
    complete_url = str(SHERDOG_URL) + url
    logger.debug("here is the search url: %s" % complete_url)
    source = urllib2.urlopen(complete_url).read()
    soup = BeautifulSoup(source)
    fightfinder_result = soup.find("table", { "class" : "fightfinder_result" })
    return fightfinder_result


def extract_link(cell):
    """extract the fight result url"""

    anchors = cell.find_all('a')
    try:
        for a in anchors:
            edited = a['href'].strip('/fighter/')
            result = ''.join([i for i in edited if not i.isdigit()])
            result = result.rstrip('-')
            return result
    except:
        return None


def extract_sherdog(cell):
    """extract the sherdog id from the link, which is usually
    a 6-9 digit number"""

    anchors = cell.find_all('a')
    try:
        for a in anchors:
            test = str(a['href'])
            edited = ''.join([i for i in test if i.isdigit()]) # the part to omit
            return edited
    except:
        return None

def extract_image(cell):
    """extract the image src url from
    the scraped page"""

    images = cell.find_all('img')
    try:
        for i in images:
            return i['src']
    except:
        return None

def create_results(fighter_info):
    """build an array for each fighter
    with the specific info required to
    create a link to their webpage"""

    search_results = {}
    search_results['bunch'] = []
    for row in fighter_info:
        cells = row.find_all('td')
        try:
            content = {
                "result_name": cells[1].get_text(),
                "result_url": extract_link(cells[1]),
                "result_sherdog_id": extract_sherdog(cells[1]),
                "result_image": extract_image(cells[0]),
            }
            
        except Exception as e:
            logger.warning("Exception")
            content = {}
        finally:
            search_results['bunch'].append(content)
    
    return search_results


@csrf_exempt
def organize(request):
    if request.method == 'POST':
        whole_url = str(request.POST['o_url'])
        try:
            edited = whole_url.strip('http://www.sherdog.com/fighter/')
            sherdog_id = str(''.join([i for i in edited if i.isdigit()]))
            fighter_name = str(''.join([i for i in edited if not i.isdigit()]))
        except Exception as e:
            logger.warning('Exception')

        info = {'fighter_name': fighter_name, 'sherdog_id': sherdog_id}
        return JsonResponse(info)


@csrf_exempt
def hunt(request):
    if request.method == 'POST':
        full_name = request.POST['surname'] +"+"+request.POST['firstName']
        logger.info ("FULL NAME POST: %s" % full_name)

        fightfinder_result = retrieve_results(full_name)
        
        # MANAGE THE EVENT OF NOT FINDING ANYTHING

        try: 
            fighter_info = fightfinder_result.find_all('tr')
        except Exception as e:
            logger.warning("no search results")
            context = {'error':'No search results found'}
            return render(request, 'ufc/search.html', context)

    search_results = create_results(fighter_info)

    # del the first result as that is the table headings
    del search_results['bunch'][0]

    context = {'links':search_results['bunch']}
    return render(request, 'ufc/search.html', context)
        

def beautiful_soup(request, fighter, sherdog_id):

    scraper = sherdog.Scraper("test")

    try:    
        history = scraper.scrape_fighter(fighter, sherdog_id)
    except Exception as e:
        raise Http404

    logger.debug(history)
    title_name = history['fighter_name']
    image_url = history['image_url']
    history_json = json.dumps(history) 
    context = {'history':history_json, 'title_name':title_name, 'image_url': image_url}
    return render(request, 'ufc/results.html', context)
