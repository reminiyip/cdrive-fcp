from __future__ import unicode_literals
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils.const import UserConst
from .utils.utils import PathUtils
from game.models import Game

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    on_screen_name = models.CharField(max_length=200, default=UserConst.DEFAULT_ON_SCREEN_NAME)
    avatar_image = models.ImageField(upload_to=PathUtils.get_avatar_file_name, default=UserConst.DEFAULT_AVATAR_IMAGE_PATH)
    accumulated_spending = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal(0.00))
    
    def __str__(self):
        return self.user.username

    def spending_required(self):
        return 100 - self.accumulated_spending

    def get_active_cart(self):
        cart = Cart.objects.get(user_id=self.user.id, status=Cart.NOT_PAID)
        return cart

    def get_purchased_games(self):
        games_id = CartGamePurchase.objects.filter(cart__user__id=self.user.id, cart__status=Cart.PAID).values_list('game', flat=True)
        games = Game.objects.filter(pk__in=set(games_id))
        return games

@receiver(post_save, sender=User)
def create_user_profile_and_cart(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, accumulated_spending=UserConst.INITIAL_ACC_SPENDING, on_screen_name=instance.username)
        Cart.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class CardPayment(models.Model):
    card_number = models.CharField(max_length=20)
    name_on_card = models.CharField(max_length=50)
    expiration_date = models.DateField()
    security_code = models.PositiveSmallIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))
    paid_date = models.DateField()

class Cart(models.Model):
    NOT_PAID = 'N'
    PROCESSING = 'PR'
    PAID = 'P'
    CART_STATUS_CHOICES = (
        (NOT_PAID, 'NotPaid'),
        (PROCESSING, 'Processing/Pending'),
        (PAID, 'Paid'),
    )

    status = models.CharField(max_length=2, choices=CART_STATUS_CHOICES, default=NOT_PAID)
    game = models.ManyToManyField('game.Game', blank=True, through='CartGamePurchase')
    payment = models.OneToOneField('CardPayment', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
        
    def get_total(self):
        # TODO: count rewards
        return sum([game.price for game in self.game.all()])

class RewardsBatch(models.Model):
    value = models.PositiveIntegerField()
    issue_date = models.DateField()
    expiration_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def issue(self):
        self.issue_date = timezone.now()
        self.expiration_date = self.issue_date + timedelta(days=RewardsConst.EXPIRE_THRESHOLD)
        self.save()

class CartGamePurchase(models.Model):
    cart = models.ForeignKey('Cart')
    game = models.ForeignKey('game.Game')
    rewards = models.PositiveSmallIntegerField(default=0)
