# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-11 20:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_auto_20170411_0226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_issue_date',
            field=models.DateTimeField(),
        ),
    ]
