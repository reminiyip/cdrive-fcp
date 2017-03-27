from django.shortcuts import render

##############################################################################
#                                       test                                 #
##############################################################################

def index(request):
    return render(request, 'core/index.html', {'data': {'test': 'I am a test string.'}})

##############################################################################
#                                      account                               #
##############################################################################



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

def view_cart_payment(request, cart_id):
    return render(request, 'core/index.html', {'data': {'cart_id': cart_id, 'action': 'view_cart_payment'}})

##############################################################################
#                                     others                                 #
##############################################################################

def view_purchase_history(request):
    return render(request, 'core/index.html', {'data': {'action': 'view_purchase_history'}})