# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ufc', '0014_auto_20150502_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opponent',
            name='value',
            field=models.IntegerField(default=10, null=True),
            preserve_default=True,
        ),
    ]
