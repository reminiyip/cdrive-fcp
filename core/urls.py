from django.conf.urls import url, include
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from . import views
from .views import CartDetailView

account_urls = [
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^', include('registration.backends.simple.urls')),
]

profile_urls = [
    url(r'^profile/$', views.view_profile, name='profile'),
    url(r'^profile/edit/', views.edit_profile, name='edit_profile'),
]

cart_urls = [
    url(r'^cart/(?P<pk>\d+)/$', CartDetailView.as_view(), name='cart'),
    url(r'^cart/(?P<cart_id>\d+)/payment/', views.payment, name='payment'),
]

other_urls = [
    url(r'^purchase_history/', views.view_purchase_history, name='purchase_history'), 
    url(r'^cart/(?P<cart_id>\d+)/assign_rewards/(?P<game_id>\d+)/(?P<reward_value>\d+)/$', views.assign_rewards_to_game, name='assign_rewards_to_game'),
]

urlpatterns = account_urls + profile_urls + cart_urls + other_urls
