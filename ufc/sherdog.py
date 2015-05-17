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

class Scraper(object):
    """docstring for Sherdog"""
    def __init__(self, arg):
        super(Scraper, self).__init__()
        self.arg = arg
        self.base_url = SHERDOG_URL
        self.fighter_url = FIGHTER_URL

    def check_db_for_fighter(self, fighter_name):
        if Fighter.objects.filter(fighter_name = fighter_name).exists():
            return True
        else:
            return False

    def load_from_db(self, fighter_name):
        if self.check_db_for_fighter(fighter_name) == True:
            # load from db
            logger.debug("LOAD FROM DB")
            obj = [{
            'fighter_name': b.fighter_name,
            'sherdog_id': b.sherdog_id,
            'value': b.value,
            'image_url': b.image_url,
            'f_url': b.f_url,
            'wins': b.wins,
            'losses': b.losses,
            'draws': b.draws,
            'weight_kg': b.weight_kg,
            'nationality': b.nationality,
            'children': [{
            'opponent': a.opponent,
            'win_loss': a.win_loss, 
            '_event': a._event, 
            'date': a.date, 
            'method_general': a.method_general,
            'method_specific': a.method_specific,
            'referee': a.referee,
            'o_url': a.o_url, 
            'sherdog_id': a.sherdog_id,
            '_round': a._round, 
            'total_time': a.total_time, 
            'value': a.value } for a in b.children.all()]} for b in Fighter.objects.filter(fighter_name=fighter_name).prefetch_related('children')]
            return obj[0]
        else: 
            return False

    def scrape_fighter(self, name, sherdog_id):

        name = str(name)
        fighter_id = str(sherdog_id)
        base_url = str(self.base_url)
        clean_name = name.replace("-", " ")

        logger.info('Something went wrong!')

        # check if fighter is in the DB, if it is return the data"""
        load_check = self.check_db_for_fighter(clean_name)
        logger.info('LOAD CHECK', load_check)

        if load_check == True:
            data = self.load_from_db(clean_name)
            return data
        else:
            """Fighter not in DB, so retrieve and parse a fighter's details from sherdog.com"""

            test_history = Fighter.objects.filter(fighter_name = clean_name)

            # fetch the required url and capture the fighter data
            history = self.process_fighter('/fighter/%s-%s' % (name, sherdog_id), sherdog_id)

            # At this point we've captured the data 
            # let's save it to the DB IF it is new TODO: improve check
            if self.check_db_for_fighter(clean_name) == False:

                full_name = str(history['fighter_name']).split(' ')

                fn = full_name[0]
                sn = full_name[1]

                a_fighter = Fighter(
                    fighter_name = history['fighter_name'],
                    first_name = fn,
                    surname_name = sn,
                    nationality = history['nationality'],
                    height_cm = float(history['height_cm']),
                    weight_kg = float(history['weight_kg']),
                    wins = history['wins'],
                    losses = history['losses'],
                    draws = history['draws'],
                    sherdog_id = history['sherdog_id'],
                    image_url = history['image_url'],
                    f_url = history['f_url']
                    )

                logger.debug("FIGHTER TO SAVE:", a_fighter)

                a_fighter.save()

                # we have to create the opponents and save them before we can add them
                
                how_many = len(history['children'])
                
                all_opponents = []

                for i in range(how_many):
                    o = Opponent(
                        opponent = history['children'][i]['opponent'],
                        win_loss = history['children'][i]['win_loss'],
                        _event = history['children'][i]['_event'],
                        #date = history['children'][i]['date'], TODO
                        method_general = history['children'][i]['method_general'],
                        method_specific = history['children'][i]['method_specific'],
                        referee = history['children'][i]['referee'],
                        _round = history['children'][i]['_round'],
                        #round_time = history['children'][i]['round_time'], TODO
                        total_time = history['children'][i]['total_time'],
                        value = history['children'][i]['value'],
                        sherdog_id = history['children'][i]['sherdog_id'],
                        o_url = history['children'][i]['o_url']
                        )
                    o.save()
                    a_fighter.children.add(o)
                    all_opponents.append(o)


        
        # This is what gets saved to the DB
        
        obj = [{
        'fighter_name': b.fighter_name, 
        'sherdog_id': b.sherdog_id, 
        'value': b.value,
        'image_url': b.image_url, 
        'f_url': b.f_url, 
        'wins': b.wins, 
        'losses': b.losses, 
        'draws': b.draws,
        'weight_kg': b.weight_kg, 
        'nationality': b.nationality,
        'children': [{
        'opponent': a.opponent, 
        'win_loss': a.win_loss, 
        '_event': a._event, 
        'date': a.date, 
        'method_general': a.method_general,
        'method_specific': a.method_specific, 
        'referee': a.referee,
        'o_url': a.o_url, 
        'sherdog_id': sherdog_id,
        '_round': a._round, 
        'total_time': a.total_time, 
        'value': a.value } for a in b.children.all()]} for b in Fighter.objects.filter(fighter_name=clean_name).prefetch_related('children')]



        logger.debug("DATA HAS BEEN SCRAPED")
        return history


    def process_fighter(self, url, sherdog_id):

        """Fetch a url and return its contents as a string"""
        
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
                    date_string = date_string

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


        def extract_mini_link(cell):
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

        def extract_full_link(cell):
            anchors = cell.find_all('a')
            try:
                for a in anchors:
                    edited = self.base_url + a['href']
                    logger.debug('edited', edited)
                    return edited
            except:
                logger.warning('error')
                return None


        def extract_sherdog(cell):
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

        def extract_image(cell):
            images = cell.find_all('img')
            try:
                for i in images:
                    return i['src']
            except:
                logger.warning('exception')
                return None


        records = {}
        """
        1 = Ronda OK, 0 = Lyoto OK
        This is because there is an upcoming event for Ronda
        We must make sure the table is correct.
        It should have this initial HTML:
        <table border="1">
            <tr class="table_head">
                <td class="col_one">Result</td>
                <td  class="col_two">Fighter</td>
                <td  class="col_three">Event</td>
                <td  class="col_four">Method/Referee</td>
                <td  class="col_five">R</td>
                <td  class="col_six">Time</td>
            </tr>
        """

        # FIND CORRECT TABLE ELEMENT
        def get_table_number(soup):
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


        table_number = get_table_number(soup)
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
                "_event": getEvent(cells[2].get_text()),
                "date": getDate(cells[2].get_text()),
                "method_general": get_general_method(cells[3].get_text()),
                "method_specific": get_specific_method(cells[3].get_text()),
                "referee": get_ref(cells[3].get_text()),
                "_round": cells[4].get_text(),
                "round_time": cells[5].get_text(),
                "total_time": get_total_time(cells[5].get_text(), cells[4].get_text()),
                "value": get_total_time(cells[5].get_text(), cells[4].get_text()),
                "o_url": extract_full_link(cells[1]), # for our purposes here, should make this the FULL url
                "sherdog_id": extract_sherdog(cells[1]),
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
