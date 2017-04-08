from django.contrib import admin

from .models import UserProfile, Cart, CardPayment, RewardsBatch, CartGamePurchase

admin.site.register(UserProfile) 
admin.site.register(Cart) 
admin.site.register(CardPayment)
admin.site.register(RewardsBatch)
admin.site.register(CartGamePurchase)