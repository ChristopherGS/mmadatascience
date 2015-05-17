# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ufc', '0003_auto_20150501_1049'),
    ]

    operations = [
        migrations.CreateModel(
            name='Opponent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('opponent', models.CharField(default=b'na', max_length=200)),
                ('win_loss', models.CharField(default=b'na', max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
