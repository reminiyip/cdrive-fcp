# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-12 15:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20170412_0406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardpayment',
            name='paid_date',
            field=models.DateTimeField(),
        ),
    ]