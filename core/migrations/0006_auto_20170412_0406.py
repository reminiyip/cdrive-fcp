# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-11 20:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20170408_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartgamepurchase',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='core.Cart'),
        ),
        migrations.AlterField(
            model_name='cartgamepurchase',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='game.Game'),
        ),
    ]
