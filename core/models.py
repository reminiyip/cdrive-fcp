from __future__ import unicode_literals
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
import math

from cdrive_fcp.utils.const import UserConst, RewardsConst
from cdrive_fcp.utils.utils import PathUtils, HelperUtils

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    on_screen_name = models.CharField(max_length=200, default=UserConst.DEFAULT_ON_SCREEN_NAME)
    avatar_image = models.ImageField(upload_to=PathUtils.get_avatar_file_name, default=UserConst.DEFAULT_AVATAR_IMAGE_PATH)
    accumulated_spending = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal(0.00))
    
    def __str__(self):
        return self.user.username

    def increment_accumulated_spending(self, value):
        self.accumulated_spending += value
        self.save()
        return self.accumulated_spending

    def issue_rewards(self):
        rewards = math.floor(self.accumulated_spending / RewardsConst.ISSUE_REWARD_THRESHOLD)
        self.accumulated_spending %= RewardsConst.ISSUE_REWARD_THRESHOLD
        self.save()

        rewards_batch = RewardsBatch(user=self.user)
        rewards_batch.issue(rewards)

        return rewards_batch

    def spending_required(self):
        return 100 - self.accumulated_spending

    def get_active_cart(self):
        cart = Cart.objects.get(user_id=self.user.id, status=Cart.NOT_PAID)
        return cart

    def get_purchased_games_id(self, ordered=True):
        if ordered:
            games_id = CartGamePurchase.objects.filter(cart__user__id=self.user.id, cart__status=Cart.PAID).order_by('-cart__payment__paid_date').values_list('game', flat=True)
        else: 
            games_id = CartGamePurchase.objects.filter(cart__user__id=self.user.id, cart__status=Cart.PAID).values_list('game', flat=True)

        return games_id

    def get_purchased_games(self):
        from game.models import Game

        games_id = self.get_purchased_games_id(ordered=False)
        games = Game.objects.filter(pk__in=set(games_id))

        return games

    def get_purchase_history(self, ordered=True):
        if ordered:
            history = CartGamePurchase.objects.filter(cart__user__id=self.user.id, cart__status=Cart.PAID).order_by('-cart__payment__paid_date')
        else:
            history = CartGamePurchase.objects.filter(cart__user__id=self.user.id, cart__status=Cart.PAID)

        return history

    def get_posted_reviews(self):
        from game.models import Review
        posted_reviews = Review.objects.filter(user=self.user.id)
        return posted_reviews

    def get_rewards_batches(self, filter_expiration_date=timezone.now()):
        rewards_batches = RewardsBatch.objects.filter(user_id=self.user.id, expiration_date__gte=filter_expiration_date) \
                                                .values('expiration_date', 'issue_date') \
                                                .annotate(values=Sum('value')) \
                                                .order_by('expiration_date')
                                                
        return rewards_batches

    def get_rewards_total(self, filter_expiration_date=timezone.now()):
        rewards_batches = self.get_rewards_batches(filter_expiration_date=filter_expiration_date)
        total_number_of_rewards = [batch['values'] for batch in rewards_batches.all()]

        return sum(total_number_of_rewards)

    def accumulated_spending_str(self, prec=2):
        return format(self.accumulated_spending, '.{}f'.format(prec))

    def spending_required_str(self, prec=2):
        return format(self.spending_required(), '.{}f'.format(prec))

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
    paid_date = models.DateTimeField()

    def __str__(self):
        if hasattr(self, 'cart') and self.cart is not None:
            return "{} on {}".format(self.cart.user.username, self.paid_date)
        else:
            return "card_payment should not exist!"

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
    games = models.ManyToManyField('game.Game', blank=True, through='CartGamePurchase')
    payment = models.OneToOneField('CardPayment', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
        
    def __str__(self):
        if self.status == Cart.PAID:
            return "{}/ {} games purchased/ {}".format(self.user.username, self.games.count(), self.payment.paid_date)
        else:
            return "{}/ {} games in cart".format(self.user.username, self.games.count())

    def get_raw_total(self):
        return sum([game.price for game in self.games.all()])

    def get_total(self):
        subtotals = [purchase.get_subtotal() for purchase in self.purchases.all()]
        return sum(subtotals)

    def get_total_str(self, prec=2):
        return format(self.get_total(), '.{}f'.format(prec))

    def get_rewards(self, now=timezone.now()):
        reward_batches = RewardsBatch.objects.filter(user_id=self.user.id).filter(issue_date__gte=(now-timedelta(days=RewardsConst.EXPIRE_THRESHOLD)))
        rewards = [reward_batch.value for reward_batch in reward_batches]
        return min(sum(rewards), RewardsConst.MAX_REWARDS)

    def get_allowed_rewards(self):
        return self.get_rewards() - int(self.purchases.aggregate(allowed_rewards=Sum('rewards'))['allowed_rewards'])

    def get_allowed_rewards_str(self):
        return str(self.get_allowed_rewards())

class RewardsBatch(models.Model):
    value = models.PositiveIntegerField()
    issue_date = models.DateField()
    expiration_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{}: {} issued on {}".format(self.user.username, self.value, self.issue_date)

    def issue(self, value):
        self.value = value
        self.issue_date = timezone.now()
        self.expiration_date = self.issue_date + timedelta(days=RewardsConst.EXPIRE_THRESHOLD)
        self.save()

    def deduct_value(self, value):
        deducted_value = value
        if self.value >= value:
            self.value -= value
        else:
            deducted_value = self.value
            self.value = 0

        self.save()
        return deducted_value

class CartGamePurchase(models.Model):
    cart = models.ForeignKey('Cart', related_name='purchases')
    game = models.ForeignKey('game.Game', related_name='purchases')
    rewards = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        if self.cart.status == Cart.PAID:
            return "{}/ {} purchased on {}".format(self.cart.user.username, self.game.title, self.cart.payment.paid_date)
        else:
            return "{}/ {} in cart".format(self.cart.user.username, self.game.title)

    def get_subtotal(self):
        return HelperUtils.get_subtotal(self.game.price, self.rewards)

    def get_subtotal_str(self):
        return HelperUtils.get_subtotal_str(self.game.price, self.rewards)

    def make_purchase(self, filter_expiration_date=timezone.now()):
        user = self.cart.user
        rewards = self.rewards
        rewards_batches = RewardsBatch.objects.filter(user_id=user.id, expiration_date__gte=filter_expiration_date).order_by('expiration_date')
        i = 0

        while rewards > 0 and i < rewards_batches.count():
            deducted_value = rewards_batches[i].deduct_value(rewards)
            rewards -= deducted_value
            i += 1

        return True if rewards == 0 else False
