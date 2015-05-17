# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ufc', '0004_opponent'),
    ]

    operations = [
        migrations.AddField(
            model_name='fighter',
            name='opponents',
            field=models.ManyToManyField(to='ufc.Opponent'),
            preserve_default=True,
        ),
    ]
