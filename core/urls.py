from django.conf.urls import url

from . import views

account_urls = [
    url(r'^register/$', views.view_register, name='register'),
    url(r'^login/$', views.view_login, name='login_page'),
    url(r'^recover/$', views.view_recover, name='recover'),
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
