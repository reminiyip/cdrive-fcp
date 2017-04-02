from django.shortcuts import render, redirect
from registration.signals import user_registered
from django.views.generic.detail import DetailView
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse

from .models import UserProfile, Cart, RewardsBatch

EXPIRE_THRESHOLD = 120
MAX_REWARD = 10

##############################################################################
#                                       test                                 #
##############################################################################

def index(request):
    return render(request, 'core/index.html', {'data': {'test': 'I am a test string.'}})

def goto_homepage(request):
	return redirect('homepage')

##############################################################################
#                                      account                               #
##############################################################################
 
def user_registered_callback(sender, user, request, **kwargs):
    profile = UserProfile(user=user)
    profile.save()
 
user_registered.connect(user_registered_callback)

##############################################################################
#                                     profile                                #
##############################################################################

def view_profile(request):
    return render(request, 'core/index.html', {'data': {'action': 'view_profile'}})

def edit_profile(request):
    return render(request, 'core/index.html', {'data': {'action': 'edit_profile'}})

##############################################################################
#                                       cart                                 #
##############################################################################

def view_cart(request, cart_id):
    return render(request, 'core/index.html', {'data': {'cart_id': cart_id, 'action': 'view_cart'}})

class CartDetailView(DetailView):
    model = Cart

    def get_context_data(self, **kwargs):
        context = super(CartDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()

        # form page_header dict
        layers = {
        	'Home': reverse('homepage'),
        	'My Shopping Cart': '#',
        }
        context['layers'] = layers

        # get rewards
        reward_batches = RewardsBatch.objects.filter(user_id=self.request.user.id).filter(issue_date__gte=(context['now']-timedelta(days=EXPIRE_THRESHOLD)))
        rewards = [reward_batch.value for reward_batch in reward_batches]
        context['rewards'] = min(sum(rewards), MAX_REWARD)

        return context

def view_cart_payment(request, cart_id):
    return render(request, 'core/index.html', {'data': {'cart_id': cart_id, 'action': 'view_cart_payment'}})

##############################################################################
#                                     others                                 #
##############################################################################

def view_purchase_history(request):
    return render(request, 'core/index.html', {'data': {'action': 'view_purchase_history'}})