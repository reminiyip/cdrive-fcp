from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.utils import timezone
from django.urls import reverse

from .models import Game, Genre
from core.models import Cart
from django.contrib.auth.models import User

##############################################################################
#                                       test                                 #
##############################################################################

def index(request):
    return render(request, 'game/index.html', {'data': {'test': 'I am a test string.'}})

##############################################################################
#                                    browse games                            #
##############################################################################

def view_homepage(request):
    return render(request, 'game/index.html', {'data': {'action': 'view_homepage'}})

def view_genre(request, genre_id):
    return render(request, 'game/index.html', {'data': {'genre_id': genre_id, 'action': 'view_genre'}})

def view_tagged_games(request, tag_name):
    return render(request, 'game/index.html', {'data': {'tag_name': tag_name, 'action': 'view_tagged_games'}})

def view_game(request, genre_id, game_id):
    return render(request, 'game/index.html', {'data': {'genre_id': genre_id, 'game_id': game_id, 'action': 'view_game'}})

class GameDetailView(DetailView):
    model = Game

    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()

        # get user active cart
        cart = Cart.objects.get(user_id=self.request.user.id)
        context['cart'] = cart

        # form page_header dict
        layers = {'Home': reverse('homepage')}
        layers[context['game'].genre.genre_name] = reverse('genre', args=[context['game'].genre.id])
        layers[context['game'].title] = '#'
        context['layers'] = layers

        return context

##############################################################################
#                                 game review actions                        #
##############################################################################

def view_reviews(request, genre_id, game_id):
    return render(request, 'game/index.html', {'data': {'genre_id': genre_id, 'game_id': game_id, 'action': 'view_reviews'}})

def view_review(request, genre_id, game_id, review_id):
    return render(request, 'game/index.html', {'data': {'genre_id': genre_id, 'game_id': game_id, 'review_id': review_id, 'action': 'view_review'}})

def new_review(request, genre_id, game_id):
    return render(request, 'game/index.html', {'data': {'genre_id': genre_id, 'game_id': game_id, 'action': 'new_review'}})

def edit_review(request, genre_id, game_id, review_id):
    return render(request, 'game/index.html', {'data': {'genre_id': genre_id, 'game_id': game_id, 'review_id': review_id, 'action': 'edit_review'}})

def remove_review(request, genre_id, game_id, review_id):
    return render(request, 'game/index.html', {'data': {'genre_id': genre_id, 'game_id': game_id, 'review_id': review_id, 'action': 'remove_review'}})

##############################################################################
#                                   game tag actions                         #
##############################################################################

def add_tag(request, genre_id, game_id, tag_name):
    # TODO add tag to db
    # TODO redirect to game page
    return render(request, 'game/index.html', {'data': {'genre_id': genre_id, 'game_id': game_id, 'tag_name': tag_name, 'action': 'add_tag'}})

##############################################################################
#                                 game purchase actions                      #
##############################################################################

def add_to_cart(request, genre_id, game_id):
    game = Game.objects.get(id=game_id)
    cart = Cart.objects.get(user_id=request.user.id)
    cart.game.add(game)
    cart.save()

    return redirect('game', genre_id=genre_id, pk=game_id)









