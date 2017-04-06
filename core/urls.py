from django.conf.urls import url, include
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views

from . import views
from .views import CartDetailView

account_urls = [
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', auth_views.login, {'redirect_authenticated_user': True,}, name='login'),
	url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
	url(r'^password_change/$', auth_views.password_change, name='password_change'),
	url(r'^password_change/done/$', auth_views.password_change_done, name='password_change_done'),
	url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
	url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
	url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
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
