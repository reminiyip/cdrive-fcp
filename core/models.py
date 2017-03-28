from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from decimal import Decimal

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    ACCOUNT_SOURCE_CHOICES = (
        ('O', 'Origin'),
        ('FB', 'FaceBook'),
        ('GH', 'GitHub'),
    )
    on_screen_name = models.CharField(max_length=200)
    avatar_image = models.ImageField(upload_to='avatars')
    accumulated_spending = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal(0.00))
    account_source = models.CharField(max_length=2, choices=ACCOUNT_SOURCE_CHOICES, default='O')
    token = models.CharField(max_length=200)
 
    def __unicode__(self):
        return self.user.username

class CardPayment(models.Model):
    card_number = models.CharField(max_length=20)
    expiration_date = models.DateField()
    security_code = models.PositiveSmallIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))
    paid_date = models.DateField()

class Cart(models.Model):
    CART_STATUS_CHOICES = (
        ('N', 'NotPaid'),
        ('PR', 'Processing/Pending'),
        ('P', 'Paid'),
    )
    status = models.CharField(max_length=2, choices=CART_STATUS_CHOICES, default='N')
    game = models.ManyToManyField('game.Game')
    payment = models.OneToOneField('CardPayment', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
        
    def get_total(self):
        return

class RewardsBatch(models.Model):
    value = models.PositiveIntegerField()
    issue_date = models.DateField()
    expiration_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)