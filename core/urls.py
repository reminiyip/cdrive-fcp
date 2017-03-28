from django.conf.urls import url, include
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from registration.forms import RegistrationFormTermsOfService
from registration.backends.default.views import RegistrationView

from . import views

main_urls = [
    url(r'^$', views.goto_homepage, name='goto_homepage'),
]

account_urls = [
    # url(r'^register/', RegistrationView.as_view(form_class=RegistrationFormTermsOfService)),
    url(r'^', include('registration.backends.simple.urls')),
    # url(r'^', include('django.contrib.auth.urls')),
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

urlpatterns = main_urls + account_urls + profile_urls + cart_urls + other_urls
