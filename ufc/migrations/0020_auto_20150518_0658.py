# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ufc', '0019_remove_opponent_image_url'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SearchResult',
        ),
        migrations.AlterField(
            model_name='fighter',
            name='f_url',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='fighter',
            name='fighter_name',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='fighter',
            name='first_name',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='fighter',
            name='image_url',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='fighter',
            name='nationality',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='fighter',
            name='surname_name',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='opponent',
            name='_event',
            field=models.CharField(default=None, max_length=64),
        ),
        migrations.AlterField(
            model_name='opponent',
            name='date',
            field=models.CharField(default=None, max_length=64),
        ),
        migrations.AlterField(
            model_name='opponent',
            name='method_general',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='opponent',
            name='method_specific',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='opponent',
            name='o_url',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='opponent',
            name='opponent',
            field=models.CharField(default=None, max_length=64),
        ),
        migrations.AlterField(
            model_name='opponent',
            name='referee',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='opponent',
            name='win_loss',
            field=models.CharField(default=None, max_length=64),
        ),
    ]
