# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ufc', '0008_auto_20150502_0448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fighter',
            name='fighter_name',
            field=models.CharField(default=b'na', max_length=200),
            preserve_default=True,
        ),
    ]
