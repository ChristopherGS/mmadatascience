# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ufc', '0016_auto_20150503_0352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fighter',
            name='_url',
            field=models.CharField(default=b'na', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fighter',
            name='birth_date',
            field=models.DateField(default=datetime.datetime.now, null=True, verbose_name=b'birthdate'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fighter',
            name='draws',
            field=models.IntegerField(default=0, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fighter',
            name='fighter_name',
            field=models.CharField(default=b'na', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fighter',
            name='first_name',
            field=models.CharField(default=b'na', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fighter',
            name='height_cm',
            field=models.IntegerField(default=0, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fighter',
            name='image_url',
            field=models.CharField(default=b'na', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fighter',
            name='losses',
            field=models.IntegerField(default=0, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fighter',
            name='nationality',
            field=models.CharField(default=b'na', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fighter',
            name='sherdog_id',
            field=models.IntegerField(default=0, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fighter',
            name='surname_name',
            field=models.CharField(default=b'na', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fighter',
            name='value',
            field=models.IntegerField(default=100, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fighter',
            name='weight_kg',
            field=models.IntegerField(default=0, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fighter',
            name='wins',
            field=models.IntegerField(default=0, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='opponent',
            name='_url',
            field=models.CharField(default=b'na', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='opponent',
            name='image_url',
            field=models.CharField(default=b'na', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='opponent',
            name='sherdog_id',
            field=models.IntegerField(default=0, null=True),
            preserve_default=True,
        ),
    ]
