# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ufc', '0007_auto_20150501_1251'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fighter',
            old_name='opponents',
            new_name='children',
        ),
        migrations.AlterField(
            model_name='fighter',
            name='fighter_name',
            field=models.CharField(default=b'na', unique=True, max_length=200),
            preserve_default=True,
        ),
    ]
