import json
import logging
import urllib2
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from django.core import serializers
from django.forms.models import model_to_dict

from ufc.models import Fighter, Opponent
import processor

logger = logging.getLogger(__name__)

SHERDOG_URL = 'http://www.sherdog.com'
FIGHTER_URL = 'http://www.sherdog.com/stats/fightfinder'

class Scraper(object):
    """This class handles the pure scraping
    of the data"""
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
            'value': a.value } for a in b.children.all()]} 
            for b in Fighter.objects.filter(fighter_name=fighter_name).prefetch_related('children')]
            return obj[0]
        else: 
            return False

    def scrape_fighter(self, name, sherdog_id):

        name = str(name)
        fighter_id = str(sherdog_id)
        base_url = str(self.base_url)
        clean_name = name.replace("-", " ")

        # check if fighter is in the DB, if it is return the data
        load_check = self.check_db_for_fighter(clean_name)
        logger.info('LOAD CHECK', load_check)

        if load_check == True:
            data = self.load_from_db(clean_name)
            return data
        else:
            # Fighter not in DB, so retrieve and parse a fighter's details from sherdog.com

            test_history = Fighter.objects.filter(fighter_name = clean_name)

            # fetch the required url and capture the fighter data
            tool = processor.Processor('test')
            history = tool.process_fighter('/fighter/%s-%s' % (name, sherdog_id), sherdog_id)

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
        'value': a.value }
        for a in b.children.all()]} for b in Fighter.objects.filter(fighter_name=clean_name).prefetch_related('children')]

        logger.debug("DATA HAS BEEN SCRAPED")
        return history


if __name__ == "__main__":
    pass
