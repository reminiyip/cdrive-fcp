from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Sum, Count
from django.contrib import messages
from collections import OrderedDict
from datetime import timedelta
import json

from .models import UserProfile, Cart, RewardsBatch, CartGamePurchase
from .forms import PaymentForm, RegisterForm, UserProfileForm, UserEmailForm
from cdrive_fcp.utils.const import RewardsConst, UserConst

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

        # get rewards, group by expiration date
        rewards_batches = RewardsBatch.objects.filter(user_id=self.request.user.id, expiration_date__gte=context['now']) \
                                                .values('expiration_date', 'issue_date') \
                                                .annotate(values=Sum('value')) \
                                                .order_by('expiration_date')
                                                
        context['rewards_batches'] = rewards_batches

        total_number_of_rewards = [batch['values'] for batch in rewards_batches.all()]
        context['total_number_of_rewards'] = sum(total_number_of_rewards)

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

            # cart paid
            cart.payment = payment
            cart.status = Cart.PAID
            cart.save()

            # assign new empty cart to user
            Cart.objects.create(user=request.user)

            return HttpResponseRedirect(reverse('payment_done', args=[cart_id]))

    else:
        form = PaymentForm()

    print(form.errors)
    
    return render(request, 'core/payment.html', {'form': form, 'cart': cart})

def payment_done(request, cart_id):
    return render(request, 'core/payment.html', {'success': True})

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

def assign_rewards_to_game(request, cart_id, game_id, reward_value):
    cg = CartGamePurchase.objects.get(game_id=game_id, cart_id=cart_id)
    cg.rewards = reward_value
    cg.save()

    return HttpResponse(reward_value)
