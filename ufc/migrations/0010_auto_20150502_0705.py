# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ufc', '0009_auto_20150502_0450'),
    ]

    operations = [
        migrations.AddField(
            model_name='fighter',
            name='value',
            field=models.IntegerField(default=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='opponent',
            name='value',
            field=models.IntegerField(default=10),
            preserve_default=True,
        ),
    ]
