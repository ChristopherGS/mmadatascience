# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ufc', '0010_auto_20150502_0705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opponent',
            name='date',
            field=models.CharField(default=b'na', max_length=200),
            preserve_default=True,
        ),
    ]
