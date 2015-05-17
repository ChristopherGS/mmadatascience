# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ufc', '0005_fighter_opponents'),
    ]

    operations = [
        migrations.AddField(
            model_name='opponent',
            name='_event',
            field=models.CharField(default=b'na', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='opponent',
            name='_round',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='opponent',
            name='date',
            field=models.DateField(default=datetime.datetime.now, verbose_name=b'birthdate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='opponent',
            name='method_general',
            field=models.CharField(default=b'na', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='opponent',
            name='method_specific',
            field=models.CharField(default=b'na', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='opponent',
            name='referee',
            field=models.CharField(default=b'na', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='opponent',
            name='round_time',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='opponent',
            name='total_time',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='opponent',
            name='value',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
