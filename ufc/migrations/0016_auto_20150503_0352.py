# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ufc', '0015_auto_20150502_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='fighter',
            name='_url',
            field=models.CharField(default=b'na', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fighter',
            name='image_url',
            field=models.CharField(default=b'na', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='opponent',
            name='_url',
            field=models.CharField(default=b'na', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='opponent',
            name='image_url',
            field=models.CharField(default=b'na', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='opponent',
            name='sherdog_id',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
