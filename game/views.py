from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.utils import timezone
from django.urls import reverse
from collections import OrderedDict

from .models import Game, Genre, Tag
from core.models import Cart, CartGamePurchase
from django.contrib.auth.models import User

##############################################################################
#                                       test                                 #
##############################################################################

def index(request):
    return render(request, 'game/index.html', {'data': {'test': 'I am a test string.'}})

##############################################################################
#                                    browse games                            #
##############################################################################

def homepage(request):
    genres = Genre.objects.all()
    genre_groups = [genres[i:i+2] for i in range(0, len(genres), 2)]
    layers = {'Home': '#'}

    return render(request, 'game/homepage.html', {'genres': genre_groups, 'layers': layers})

def view_genre(request, genre_id):
    return render(request, 'game/index.html', {'data': {'genre_id': genre_id, 'action': 'view_genre'}})

class GenreDetailView(DetailView):
    model = Genre

    def get_context_data(self, **kwargs):
        context = super(GenreDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()

        # # get games, group by 2
        games = Game.objects.filter(genre_id=context['genre'].id)
        context['games'] = [games[i:i+2] for i in range(0, len(games), 2)]

        # form page_header dict
        layers = OrderedDict()
        layers['Home'] = reverse('homepage')
        layers[context['genre'].genre_name] = '#'
        context['layers'] = layers

        return context

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
        cart = self.request.user.profile.get_active_cart()
        context['cart'] = cart
        
        # get game tags
        tags = context['game'].get_sorted_tags()
        context['tags'] = tags

        # form page_header dict
        layers = OrderedDict()
        layers['Home'] = reverse('homepage')
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
#                                      actions                               #
##############################################################################

def add_tag(request, genre_id, game_id):
    if request.method == 'POST':
        req_tag_name = request.POST.get('tag_name', None)
        
        if not req_tag_name == "":
            tag_game = Game.objects.get(id=game_id)

            # add new tag to db
            if not Tag.objects.filter(tag_name=req_tag_name, game=tag_game).exists():
                tag = Tag(tag_name=req_tag_name, popularity=1, game=tag_game)
                tag.save()

            # increment popularity
            else:
                tag = Tag.objects.get(tag_name=req_tag_name, game=tag_game)
                tag.increment_popularity()
    
    # redirect to game page
    return redirect('game', genre_id=genre_id, pk=game_id)

def add_to_cart(request, genre_id, game_id):
    cart = request.user.profile.get_active_cart()
    cg = CartGamePurchase(game_id=game_id, cart_id=cart.id)
    cg.save()

    return redirect('game', genre_id=genre_id, pk=game_id)









