# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-01-03 13:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('codestreak', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='streak',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 3, 13, 17, 48, 923656, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
