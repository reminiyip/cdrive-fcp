# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-10 18:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_genre_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_issue_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 10, 18, 26, 13, 892208, tzinfo=utc)),
        ),
    ]
