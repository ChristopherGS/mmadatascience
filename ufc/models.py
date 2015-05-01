from django.db import models
from datetime import datetime

# Create your models here.


# Many to many relationship (I presume?) because a fighter can have many opponents, and an opponent has fought many fighters.

class Opponent(models.Model):
	opponent = models.CharField(max_length=200, default="na")
	win_loss = models.CharField(max_length=200, default="na")
	_event = models.CharField(max_length=200, default="na")

	date = models.DateField('date', default=datetime.now)

	method_general = models.CharField(max_length=200, default="na")
	method_specific = models.CharField(max_length=200, default="na")
	referee = models.CharField(max_length=200, default="na")
	_round = models.IntegerField(default=0)

	#round_time = birth_date = models.TimeField(default=00)
	total_time = models.IntegerField(default=0)
	
	value = models.IntegerField(default=0)

	def __unicode__(self): # __str__ on Python 3
		return self.opponent


class Fighter(models.Model):
	
	fighter_name = models.CharField(max_length=200, default="na", unique=True)
	first_name = models.CharField(max_length=200, default="na")
	surname_name = models.CharField(max_length=200, default="na")

	birth_date = models.DateField('birthdate', default=datetime.now)
	nationality = models.CharField(max_length=200, default="na")
	height_cm = models.IntegerField(default=0)
	weight_kg = models.IntegerField(default=0)
	sherdog_id = models.IntegerField(default=0)
	wins = models.IntegerField(default=0)
	losses = models.IntegerField(default=0)
	draws = models.IntegerField(default=0)

	opponents = models.ManyToManyField(Opponent)
	

	def __unicode__(self): # __str__ on Python 3
		return self.fighter_name

	class Admin:
		pass


class SearchResult(models.Model):
	search_data = models.CharField(max_length=200)

	def __unicode__(self): # __str__ on Python 3
		return self.search_data

		"""
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

		d3 = {}
		d3['name'] = result['name']
		d3['value'] = 100 #should be total career fight time in seconds TODO
		d3['total_fight_time'] = 
		"""