from django.conf.urls import url, include
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from . import views
from .views import CartDetailView

account_urls = [
    # url(r'^register/', RegistrationView.as_view(form_class=RegistrationFormTermsOfService)),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^', include('registration.backends.simple.urls')),
]

profile_urls = [
    url(r'^profile/$', views.view_profile, name='profile'),
    url(r'^profile/edit/', views.edit_profile, name='edit_profile'),
]

cart_urls = [
    url(r'^cart/(?P<pk>\d+)/$', CartDetailView.as_view(), name='cart'),
    url(r'^cart/(?P<cart_id>\d+)/payment/', views.view_cart_payment, name='cart_payment'),
]

other_urls = [
    url(r'^purchase_history/', views.view_purchase_history, name='purchase_history'), 
]

urlpatterns = account_urls + profile_urls + cart_urls + other_urls
