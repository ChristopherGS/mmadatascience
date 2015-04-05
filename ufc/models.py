from django.db import models

# Create your models here.

class Fighter(models.Model):
	fighter_name = models.CharField(max_length=200)


	def __unicode__(self): # __str__ on Python 3
		return self.fighter_name


class SearchResult(models.Model):
	search_data = models.CharField(max_length=200)

	def __unicode__(self): # __str__ on Python 3
		return self.search_data