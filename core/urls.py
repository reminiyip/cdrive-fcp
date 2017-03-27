from django.conf.urls import url, include
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from . import views

account_urls = [
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^register/', CreateView.as_view(
        template_name='registration/register.html',
        form_class=UserCreationForm,
        success_url='/'
    )),
]

profile_urls = [
    url(r'^profile/$', views.view_profile, name='profile'),
    url(r'^profile/edit/', views.edit_profile, name='edit_profile'),
]

cart_urls = [
    url(r'^cart/(?P<cart_id>\d+)/$', views.view_cart, name='cart'),
    url(r'^cart/(?P<cart_id>\d+)/payment/', views.view_cart_payment, name='cart_payment'),
]

other_urls = [
    url(r'^purchase_history/', views.view_purchase_history, name='purchase_history'), 
]

urlpatterns = account_urls + profile_urls + cart_urls + other_urls
