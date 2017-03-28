from django.contrib import admin

from .models import User, Cart, CardPayment, RewardsBatch

admin.site.register(User) 
admin.site.register(Cart) 
admin.site.register(CardPayment)
admin.site.register(RewardsBatch)