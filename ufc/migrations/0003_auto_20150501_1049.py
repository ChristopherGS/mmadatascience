# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ufc', '0002_searchresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='fighter',
            name='birth_date',
            field=models.DateField(default=datetime.datetime.now, verbose_name=b'birthdate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fighter',
            name='draws',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fighter',
            name='first_name',
            field=models.CharField(default=b'na', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fighter',
            name='height_cm',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fighter',
            name='losses',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fighter',
            name='nationality',
            field=models.CharField(default=b'na', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fighter',
            name='sherdog_id',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fighter',
            name='surname_name',
            field=models.CharField(default=b'na', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fighter',
            name='weight_kg',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fighter',
            name='wins',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fighter',
            name='fighter_name',
            field=models.CharField(default=b'na', max_length=200),
            preserve_default=True,
        ),
    ]
