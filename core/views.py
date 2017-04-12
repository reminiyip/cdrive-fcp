from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.db.models import Sum
from collections import OrderedDict
from datetime import timedelta
import json

from .models import UserProfile, Cart, RewardsBatch, CartGamePurchase
from game.models import Game
from .forms import PaymentForm, RegisterForm, UserProfileForm, UserEmailForm
from cdrive_fcp.utils.const import UserConst, RewardsConst
from cdrive_fcp.utils.utils import HelperUtils, EmailUtils

##############################################################################
#                                       test                                 #
##############################################################################

def index(request):
    return render(request, 'core/index.html', {'data': {'test': 'I am a test string.'}})

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

class ProfileDetailView(DetailView):
    model = UserProfile

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()

        # form page_header dict
        layers = OrderedDict()
        layers['Home'] = reverse('homepage')
        layers['My Profile'] = '#'
        context['layers'] = layers
                                         
        # get rewards info
        context['rewards_batches'] = self.request.user.profile.get_rewards_batches()
        context['total_number_of_rewards'] = self.request.user.profile.get_rewards_total()

        return context

def edit_profile(request, profile_id):
    if request.method == 'POST':
        user_email_form = UserEmailForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_email_form.is_valid() and profile_form.is_valid():
            user_email_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')

            return redirect('profile', profile_id)

        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        user_email_form = UserEmailForm(instance=request.user, label_suffix='')
        profile_form = UserProfileForm(instance=request.user.profile, label_suffix='')

        # form page_header dict
        layers = OrderedDict()
        layers['Home'] = reverse('homepage')
        layers['My Profile'] = '#'

    return render(request, 'core/edit_profile.html', {
        'action': 'edit',
        'user_email_form': user_email_form,
        'profile_form': profile_form,
        'layers': layers,
    })

##############################################################################
#                                       cart                                 #
##############################################################################

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

            # cart paid
            cart.payment = payment
            cart.status = Cart.PAID
            cart.save()

            return HttpResponseRedirect(reverse('payment_done', args=[cart_id]))

    else:
        form = PaymentForm()
    
    return render(request, 'core/payment.html', {'form': form, 'cart': cart})

def payment_done(request, cart_id):
    cart = Cart.objects.get(pk=cart_id)

    # rewards used
    purchases = cart.purchases
    for purchase in purchases.all():
        if not purchase.make_purchase(filter_expiration_date=cart.payment.paid_date):
            print("Cannot make purchase")

    # clean rewards batches; delete expired and value = 0 batches
    RewardsBatch.objects.filter(user_id=request.user.id, expiration_date__lt=cart.payment.paid_date).delete()
    RewardsBatch.objects.filter(user_id=request.user.id, value=0).delete()

    # assign new empty cart to user
    Cart.objects.create(user=request.user)

    # add accumulated spending to user
    accumulated_spending = request.user.profile.increment_accumulated_spending(cart.get_total())

    # check accumulated spending to send new rewards
    rewards = None
    if accumulated_spending >= RewardsConst.ISSUE_REWARD_THRESHOLD:
        rewards = request.user.profile.issue_rewards()

    EmailUtils.confirm_purchase(request.user, cart_id, rewards=rewards)

    return render(request, 'core/payment_done.html')

##############################################################################
#                                     others                                 #
##############################################################################

def purchase_history(request):
    records = request.user.profile.get_purchase_history()
    
    layers = OrderedDict()
    layers['Home'] = reverse('homepage')
    layers['Purchase History'] = '#'

    return render(request, 'core/purchase_history.html', {'records': records, 'layers': layers})


##############################################################################
#                                     actions                                #
##############################################################################

def assign_rewards_to_game(request, cart_id):
    game_id = request.GET.get('game')
    reward_value = request.GET.get('value')

    game = Game.objects.get(pk=game_id)
    cart = Cart.objects.get(pk=cart_id)
    total_rewards = cart.get_rewards()

    cg = CartGamePurchase.objects.get(game_id=game_id, cart_id=cart_id)
    cg.rewards = reward_value
    cg.save()

    discount = HelperUtils.get_discount_str(game.price, reward_value)
    subtotal = HelperUtils.get_subtotal_str(game.price, reward_value)
    total = Cart.objects.get(pk=cart_id).get_total_str()
    allowed_rewards = cart.get_allowed_rewards()

    return HttpResponse(json.dumps({'reward_value': reward_value, 'discount': discount, 'subtotal': subtotal, 'total': total, 'allowed_rewards': allowed_rewards}))

def cart_remove_game(request, cart_id, game_id):
    CartGamePurchase.objects.get(cart_id=cart_id, game_id=game_id).delete()

    return redirect('cart', cart_id)






