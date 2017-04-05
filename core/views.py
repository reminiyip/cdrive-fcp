from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponse
from collections import OrderedDict
from datetime import timedelta
import json

from .models import UserProfile, Cart, RewardsBatch, CartGamePurchase
from .forms import PaymentForm, RegisterForm, UserProfileForm, UserEmailForm
from .utils.const import RewardsConst, UserConst

from django.contrib import messages
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

def register(request):
    if request.user.is_authenticated():
        return redirect('homepage')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('homepage')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


##############################################################################
#                                     profile                                #
##############################################################################

def view_profile(request):
    return render(request, 'core/profile.html', {'data': {'action': 'view_profile'}})

def edit_profile(request):
    if request.method == 'POST':
        user_email_form = UserEmailForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_email_form.is_valid() and profile_form.is_valid():
            user_email_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')

    else:
        user_email_form = UserEmailForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    return render(request, 'core/edit_profile.html', {
        'user_email_form': user_email_form,
        'profile_form': profile_form
    })

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
