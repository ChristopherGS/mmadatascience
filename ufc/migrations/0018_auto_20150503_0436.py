# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ufc', '0017_auto_20150503_0417'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fighter',
            old_name='_url',
            new_name='f_url',
        ),
        migrations.RenameField(
            model_name='opponent',
            old_name='_url',
            new_name='o_url',
        ),
    ]
