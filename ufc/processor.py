import json
import logging
import urllib2
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from django.core import serializers
from django.forms.models import model_to_dict

from ufc.models import Fighter, Opponent

logger = logging.getLogger(__name__)
SHERDOG_URL = 'http://www.sherdog.com'
FIGHTER_URL = 'http://www.sherdog.com/stats/fightfinder'


class Processor(object):
    """Handles the processing and saving
    of the fighter records"""
    def __init__(self, arg):
        super(Processor, self).__init__()
        self.arg = arg
        self.base_url = SHERDOG_URL
        self.fighter_url = FIGHTER_URL

    def get_event(self, eventString):
            dateStrings = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            for x in dateStrings:
                index = eventString.find(x)
                if (index == -1):
                    pass
                else:
                    return eventString[:index]

    def get_general_method(self, eventString):
        index = eventString.find('(')
        if (index == -1):
            pass
        else:
            general_method = eventString[:index].rstrip()
            return general_method

    def get_specific_method(self, eventString):
        index = eventString.find('(')
        end_index = eventString.find(')')
        if (index == -1):
            pass
        else:
            specific_method = eventString[index+1:end_index].rstrip()
            return specific_method

    def get_ref(self, eventString):
            index = eventString.find(')')
            if (index == -1):
                pass
            else:
                return eventString[index+1:]

    def get_sec(self, s):
        convert_to_string = str(s)
        l = convert_to_string.split(':')
        return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])

    def get_total_time(self, time, tround):
        
        try:
            around = int(tround)
            the_round = around 

            the_time = datetime.strptime(time, '%M:%S').time()
            the_time = self.get_sec(the_time)
            
            total_fight_time = 0


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
            logger.warning("Exception motherfucker!:", e)
            logger.info("time", time, type(time))
            logger.info("round", tround, type(tround))
            pass


    def extract_mini_link(self, cell):
        """extracts just the fighter name section
        of url
        """
        anchors = cell.find_all('a')
        try:
            for a in anchors:
                edited = a['href'].strip('/fighter/')
                result = ''.join([i for i in edited if not i.isdigit()])
                result = result.rstrip('-')
                logger.debug("edited", result)
                return result
        except:
            logger.warning('error')
            return None

    def extract_full_link(self, cell):
        anchors = cell.find_all('a')
        try:
            for a in anchors:
                edited = self.base_url + a['href']
                logger.debug('edited', edited)
                return edited
        except:
            logger.warning('error')
            return None

    def extract_sherdog(self, cell):
        anchors = cell.find_all('a')
        try:
            for a in anchors:
                test = str(a['href'])
                edited = ''.join([i for i in test if i.isdigit()]) # the part to omit
                logger.debug(edited)
                return edited
        except:
            logger.warning('exception')
            return None

    def extract_image(self, cell):
        images = cell.find_all('img')
        try:
            for i in images:
                return i['src']
        except:
            logger.warning('exception')
            return None

    # FIND CORRECT TABLE ELEMENT
    def get_table_number(self, soup):
        correct_table = 0 # sensible default
        for i in range(5):
            find_right_table = soup.findAll('table')[i].findAll('tr')
            for row in find_right_table:
                cells = row.find_all('td')
                try:
                    if cells[0].get_text() == "Result" and cells[1].get_text() == "Fighter" and cells[3].get_text() == "Method/Referee":
                        correct_table = i
                        logger.debug("The correct table number is: ", correct_table) 
                        return correct_table
                except Exception as e:
                    logger.warning("incorrect table")
                finally:
                    i = i + 1
        
    def process_fighter(self, url, sherdog_id):

        """create the fighter object to send back to the sherdog.py"""

        print "HERE AT PROCESS FIGHTER"
        
        updated_url = str(self.base_url) + url
        logger.debug("here is the url: %s" % updated_url)

        source = urllib2.urlopen(updated_url).read()
        soup = BeautifulSoup(source)

        fighter_name = soup.find_all("span", class_="fn")
        fighter_namey = soup.find('h1', {'itemprop': 'name'}).span.contents[0]

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

        profile_image = soup.find('img', {'class': 'profile_image photo'})
        image_url = profile_image["src"]

        # build a dict with the scraped data and return it for use later
        result = {
            'name': fighter_namey,
            'birth_date': birth_date,
            'locality': locality,
            'nationality': nationality,
            'height_cm': height_cm,
            'weight_kg': weight_kg,
            'camp_team': camp_team,
            'wins': wld['wins'],
            'losses': wld['losses'],
            'draws': wld['draws'],
            'last_fight': last_fight,
            'sherdog_id': sherdog_id,
            '_url': updated_url,
            'image_url': image_url
            }

        def get_my_date(eventString):
            dateStrings = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            conflicts = ["Jungle", "Maynard", "Mayhem", "March"]

            for x in conflicts:
                edge_case = eventString.find(x)
                if (edge_case != -1):
                    return "*No date   " # hack

            for x in dateStrings: # loop through date strings
                # attempt to find one of the list items in the function argument
                index = eventString.find(x) 

                if (index == -1):
                    pass
                else:
                    date_string = eventString[index:]
                    date_string = date_string.replace(" / ", "-")

                    try: 
                        actual_date = datetime.strptime(date_string, '%b-%d-%Y')
                        json_date = json.dumps(actual_date, default=json_serial)
                    except Exception as e:
                        logger.warning('ERROR', e)
                        json_date = None

                    return json_date

        def json_serial(obj):
            if isinstance (obj, datetime):
                serial = obj.isoformat()
                return serial
        
        """
        1 = Ronda OK, 0 = Lyoto OK
        This is because there is an upcoming event for Ronda
        """

        records = {}
        table_number = self.get_table_number(soup)
        records = soup.findAll('table')[table_number].findAll('tr')
        
        """
        This is where the scraped object is built
        the data from "result" is lost after this
        """

        d3 = {}
        d3['fighter_name'] = result['name']
        d3['birth_date'] = result['birth_date']
        d3['locality'] = result['locality']
        d3['nationality'] = result['nationality']
        d3['height_cm'] = result['height_cm']
        d3['weight_kg'] = result['weight_kg']
        d3['wins'] = result['wins']
        d3['losses'] = result['losses']
        d3['draws'] = result['draws']
        d3['sherdog_id'] = result['sherdog_id']
        d3['f_url'] = result['_url']
        d3['image_url'] = result['image_url']


        d3['value'] = 100 # should be total career fight time in seconds TODO
        d3['total_fight_time'] = ""
        d3['children'] = []
        content = []
        
        for row in records:
            cells = row.find_all('td')

            content = {

                "opponent": cells[1].get_text(),
                "win_loss": cells[0].get_text(),
                "_event": self.get_event(cells[2].get_text()),
                "date": get_my_date(cells[2].get_text()),
                "method_general": self.get_general_method(cells[3].get_text()),
                "method_specific": self.get_specific_method(cells[3].get_text()),
                "referee": self.get_ref(cells[3].get_text()),
                "_round": cells[4].get_text(),
                "round_time": cells[5].get_text(),
                "total_time": self.get_total_time(cells[5].get_text(), cells[4].get_text()),
                "value": self.get_total_time(cells[5].get_text(), cells[4].get_text()),
                "o_url": self.extract_full_link(cells[1]), # for our purposes here, should make this the FULL url
                "sherdog_id": self.extract_sherdog(cells[1]),
                # "image_url": extract_image(cells[0]), #more complex
            }

            d3['children'].append(content)
            
        def clean_up(history):
            # remove the first entry as these are just row titles
            d3['children'].pop(0) 

        clean_up(d3)

        # now let's create the total career time

        def calc_career_time():
            career_time = 0
            for duration in d3['children']:
                for key, value in duration.iteritems():
                    if key == "total_time":
                        try:
                            career_time += value
                        except:
                            pass
            d3['total_fight_time'] = career_time
            d3['value'] = career_time


        calc_career_time()

        return d3






if __name__ == "__main__":
    pass