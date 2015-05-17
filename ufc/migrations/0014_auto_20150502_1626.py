# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ufc', '0013_auto_20150502_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opponent',
            name='total_time',
            field=models.IntegerField(default=0, null=True),
            preserve_default=True,
        ),
    ]
