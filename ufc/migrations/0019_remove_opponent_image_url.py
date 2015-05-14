# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ufc', '0018_auto_20150503_0436'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opponent',
            name='image_url',
        ),
    ]
