from __future__ import unicode_literals

from django.db import models

# Create your models here.

Class User():
    user_name
    password
    email_address
    on_screen_name
    avatar_image
    accumulated_spending
    carts
    rewards
    account_source
    token
    
    def make_new_cart(self):
        
    def make_new_rewards(self):
    

Class Rewards(models.Model):
    reward_id = models.PositiveIntegerField()
    value = models.PositiveIntegerField()
    issue_date = models.DateField()
    expiration_date = models.DateField()

Class CardPayment
    card_number = models.PositiveIntegerField()
    expiration_date = models.DateField()
    security_code = models.PositiveSmallIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_date = models.DateField()

Class Cart
    cart_id = models.IntegerField()
    status = models.CharField(max_length=15)
    games = models.ManyToManyField(Game)
    payment = models.ForeignKey(CardPayment, on_delete=models.CASCADE)
    
    def add_game(self,game):
        
    def make_payment(self):
        
    def get_total(self):
 
