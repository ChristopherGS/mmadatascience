# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ufc', '0011_auto_20150502_0710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opponent',
            name='method_general',
            field=models.CharField(default=b'na', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='opponent',
            name='method_specific',
            field=models.CharField(default=b'na', max_length=200, null=True),
            preserve_default=True,
        ),
    ]
