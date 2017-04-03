# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-03 10:12
from __future__ import unicode_literals

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('game', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CardPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=20)),
                ('name_on_card', models.CharField(max_length=50)),
                ('expiration_date', models.DateField()),
                ('security_code', models.PositiveSmallIntegerField()),
                ('amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('paid_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('N', 'NotPaid'), ('PR', 'Processing/Pending'), ('P', 'Paid')], default='N', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='CartGamePurchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rewards', models.PositiveSmallIntegerField(default=0)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Cart')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Game')),
            ],
        ),
        migrations.CreateModel(
            name='RewardsBatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveIntegerField()),
                ('issue_date', models.DateField()),
                ('expiration_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('on_screen_name', models.CharField(max_length=200)),
                ('avatar_image', models.ImageField(upload_to='avatars')),
                ('accumulated_spending', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=15)),
                ('account_source', models.CharField(choices=[('O', 'Origin'), ('FB', 'FaceBook'), ('GH', 'GitHub')], default='O', max_length=2)),
                ('token', models.CharField(max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='game',
            field=models.ManyToManyField(blank=True, through='core.CartGamePurchase', to='game.Game'),
        ),
        migrations.AddField(
            model_name='cart',
            name='payment',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.CardPayment'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
