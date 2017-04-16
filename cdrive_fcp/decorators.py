from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from core.models import UserProfile, Cart, CartGamePurchase
from game.models import Review, Game, Genre

def user_is_profile_owner(function):
	def wrap(request, *args, **kwargs):
		if('pk' in kwargs):
			profile = get_object_or_404(UserProfile, pk=kwargs['pk'])
		else:
			profile = get_object_or_404(UserProfile, pk=kwargs['profile_id'])
		if request.user.profile == profile:
			return function(request, *args, **kwargs)
		else:
			raise PermissionDenied
	return wrap

def cart_is_user_active_cart(function):
	def wrap(request, *args, **kwargs):
		if('pk' in kwargs):
			cart = get_object_or_404(Cart, pk=kwargs['pk'])
		else:
			cart = get_object_or_404(Cart, pk=kwargs['cart_id'])
		if request.user.profile.get_active_cart() == cart:
			return function(request, *args, **kwargs)
		else:
			raise PermissionDenied
	return wrap

def payment_just_saved_by_the_system(function):
	def wrap(request, *args, **kwargs):
		cart = Cart.objects.get(pk=kwargs['cart_id'])
		if cart.payment:
			return function(request, *args, **kwargs)
		else:
			raise PermissionDenied
	return wrap

def user_not_purchased_the_game_and_game_not_in_active_cart(function):
	def wrap(request, *args, **kwargs):
		game = Game.objects.get(pk=kwargs['game_id'])
		games = request.user.profile.get_active_cart().games.all()
		if (game not in games) and (game not in request.user.profile.get_purchased_games()):
			return function(request, *args, **kwargs)
		else:
			raise PermissionDenied
	return wrap

def game_is_in_active_cart(function):
	def wrap(request, *args, **kwargs):
		game = Game.objects.get(pk=kwargs['game_id'])
		games = request.user.profile.get_active_cart().games.all()
		if game in games:
			return function(request, *args, **kwargs)
		else:
			raise PermissionDenied
	return wrap

def user_purchased_the_game(function):
	def wrap(request, *args, **kwargs):
		game = Game.objects.get(pk=kwargs['game_id'])
		if game in request.user.profile.get_purchased_games():
			return function(request, *args, **kwargs)
		else:
			raise PermissionDenied
	return wrap

def user_posted_the_review(function):
	def wrap(request, *args, **kwargs):
		review = get_object_or_404(Review, pk=kwargs['review_id'])
		if review in request.user.profile.get_posted_reviews():
			return function(request, *args, **kwargs)
		else:
			raise PermissionDenied
	return wrap

def logout_required(function):
	def wrap(request, *args, **kwargs):
		if request.user.is_authenticated():
			return redirect('homepage')
		else:
			return function(request, *args, **kwargs)
	return wrap

def genre_is_valid(function):
	def wrap(request, *args, **kwargs):
		genre = get_object_or_404(Genre, pk=kwargs['genre_id'])
		return function(request, *args, **kwargs)
	return wrap

def game_is_valid(function):
	def wrap(request, *args, **kwargs):
		game = get_object_or_404(Game, pk=kwargs['game_id'])
		return function(request, *args, **kwargs)
	return wrap