# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-01-03 22:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codestreak', '0005_auto_20170103_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streak',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 3, 23, 37, 4, 270934)),
        ),
    ]