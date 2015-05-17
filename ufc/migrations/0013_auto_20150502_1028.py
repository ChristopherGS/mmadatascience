# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ufc', '0012_auto_20150502_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opponent',
            name='referee',
            field=models.CharField(default=b'na', max_length=200, null=True),
            preserve_default=True,
        ),
    ]
