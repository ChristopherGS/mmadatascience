from datetime import datetime

from django.db import models

class Opponent(models.Model):
    opponent = models.CharField(max_length=64, default=None)
    win_loss = models.CharField(max_length=64, default=None)
    _event = models.CharField(max_length=64, default=None)

    #date = models.DateField('date', default=datetime.now)
    date = models.CharField(max_length=64, default=None)
    method_general = models.CharField(max_length=64, default=None, null=True)
    method_specific = models.CharField(max_length=64, default=None, null=True)
    referee = models.CharField(max_length=64, default=None, null=True)
    _round = models.IntegerField(default=0)

    #round_time = birth_date = models.TimeField(default=00)
    total_time = models.IntegerField(default=0, null=True)
    
    #for D3.js
    value = models.IntegerField(default=10, null=True)

    #for scraping

    sherdog_id = models.IntegerField(default=0, null=True)
    o_url = models.CharField(max_length=64, default=None, null=True)
    #image_url = models.CharField(max_length=64, default=None, null=True) more problematic - requires following the link

    def __unicode__(self): # __str__ on Python 3
        return self.opponent


class Fighter(models.Model):
    
    fighter_name = models.CharField(max_length=64, default=None, null=True)
    first_name = models.CharField(max_length=64, default=None, null=True)
    surname_name = models.CharField(max_length=64, default=None, null=True)
    birth_date = models.DateField('birthdate', default=datetime.now, null=True)
    nationality = models.CharField(max_length=64, default=None, null=True)
    height_cm = models.IntegerField(default=0, null=True)
    weight_kg = models.IntegerField(default=0, null=True)
    wins = models.IntegerField(default=0, null=True)
    losses = models.IntegerField(default=0, null=True)
    draws = models.IntegerField(default=0, null=True)

    #for D3.js
    value = models.IntegerField(default=100, null=True)

    #for scraping
    sherdog_id = models.IntegerField(default=0, null=True)
    f_url = models.CharField(max_length=64, default=None, null=True)
    image_url = models.CharField(max_length=64, default=None, null=True)

    #we call this field "children" to reduce d3.js conversion on the front end
    children = models.ManyToManyField(Opponent)
    

    def __unicode__(self): # __str__ on Python 3
        return self.fighter_name

    class Admin:
        pass
