from django.shortcuts import render, redirect
from registration.signals import user_registered
from django.views.generic.detail import DetailView
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponse
from collections import OrderedDict
from datetime import timedelta
import json

from .models import UserProfile, Cart, RewardsBatch, CartGamePurchase
from .forms import PaymentForm
from .utils.const import RewardsConst

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
    profile = UserProfile(user=user, accumulated_spending=UserConst.INITIAL_ACC_SPENDING)
    profile.save()

    # create new cart
    cart = Cart(user=user)
    cart.save()

 
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
        layers = OrderedDict()
        layers['Home'] = reverse('homepage')
        layers['My Shopping Cart'] = '#'
        context['layers'] = layers

        # get rewards
        reward_batches = RewardsBatch.objects.filter(user_id=self.request.user.id).filter(issue_date__gte=(context['now']-timedelta(days=RewardsConst.EXPIRE_THRESHOLD)))
        rewards = [reward_batch.value for reward_batch in reward_batches]
        context['rewards'] = min(sum(rewards), RewardsConst.MAX_REWARDS)

        return context

def payment(request, cart_id):
    cart = Cart.objects.get(pk=cart_id)

    if request.method == "POST":
        form = PaymentForm(request.POST)

        if form.is_valid():
            payment = form.save(commit=False)
            payment.amount = cart.get_total()
            payment.paid_date = timezone.now()
            payment.save()

            cart.card_payment = payment
            cart.status = Cart.PAID
            cart.save()

            return HttpResponse('OK')

        else:
            return HttpResponse(json.dumps(form.errors))

    else:
        form = PaymentForm()
        return render(request, 'core/payment.html', {'form': form, 'cart': cart})

##############################################################################
#                                     others                                 #
##############################################################################

def view_purchase_history(request):
    return render(request, 'core/index.html', {'data': {'action': 'view_purchase_history'}})

##############################################################################
#                                     actions                                #
##############################################################################

def assign_rewards_to_game(request, cart_id, game_id, reward_value):
    cg = CartGamePurchase.objects.get(game_id=game_id, cart_id=cart_id)
    cg.rewards = reward_value
    cg.save()

    return HttpResponse(reward_value)




