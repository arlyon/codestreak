# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-01-03 22:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codestreak', '0004_auto_20170103_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='streak',
            name='lost',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='streak',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 3, 23, 2, 28, 475863)),
        ),
    ]
