# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ufc', '0006_auto_20150501_1238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opponent',
            name='round_time',
        ),
        migrations.AlterField(
            model_name='opponent',
            name='date',
            field=models.DateField(default=datetime.datetime.now, verbose_name=b'date'),
            preserve_default=True,
        ),
    ]
