from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.utils import timezone, text
from django.urls import reverse
from collections import OrderedDict

from .models import Game, Genre, Tag, Platform
from core.models import Cart, CartGamePurchase
from django.contrib.auth.models import User
from cdrive_fcp.utils.utils import HelperUtils

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
    genre_groups = HelperUtils.get_column_groups(genres)
    
    # recommendations
    purchases = request.user.profile.get_purchase_history(ordered=True)
    purchased_games = []
    for purchase in purchases:
        purchased_games.append(purchase.game)
    target_num = min(3, len(purchases))
    targets = []
    sim_list = []
    for i in range(target_num):
        targets.append(purchases[i].game)
    for target in targets:
        sim_games = target.get_similar_games()
        if(len(sim_games)>0):
            while(len(sim_games)>0 and sim_games[0] in purchased_games):
                sim_games.pop(0)
        if(len(sim_games)>0):     
            sim_list.append(sim_games[0])
    recommended_games = []
    for i in sim_list:
        if i not in recommended_games:
            recommended_games.append(i)
            print(i.title)
        
    #recommended_games = list(set(sim_list))
        
    
    # layers
    layers = {'Home': '#'}

    return render(request, 'game/homepage.html', {'genres': genre_groups, 'recommendations': recommended_games, 'layers': layers})

def view_genre(request, genre_id):
    return render(request, 'game/index.html', {'data': {'genre_id': genre_id, 'action': 'view_genre'}})

class GenreDetailView(DetailView):
    model = Genre

    def get_context_data(self, **kwargs):
        context = super(GenreDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()

        # platforms
        platforms = Platform.objects.all()
        context['platforms'] = platforms

        # get filters
        if self.request.GET.get('filters') != None:
            filters = self.request.GET.get('filters').split(',')
        else:
            filters = platforms.values_list('platform_name', flat=True)
        context['filters'] = filters

        # get sorted games, group by 2
        games = Game.objects.filter(genre_id=context['genre'].id, platforms__platform_name__in=filters).distinct().order_by('-release_date')
        context['games'] = HelperUtils.get_column_groups(games)

        # form page_header dict
        layers = OrderedDict()
        layers['Home'] = reverse('homepage')
        layers[context['genre'].genre_name] = '#'
        context['layers'] = layers

        return context

def tagged_games(request, tag_name):
    # platforms
    platforms = Platform.objects.all()

    # get filters
    if request.GET.get('filters') != None:
        filters = request.GET.get('filters').split(',')
    else:
        filters = platforms.values_list('platform_name', flat=True)

    # games
    games = Game.objects.filter(tag__tag_name__contains=tag_name, platforms__platform_name__in=filters).distinct().order_by('-release_date')
    game_groups = HelperUtils.get_column_groups(games)

    # form page_header dict
    layers = OrderedDict()
    layers['Home'] = reverse('homepage')
    layers['Tag - {}'.format(tag_name)] = '#'

    return render(request, 'game/tag.html', {'games': game_groups, 'tag_name': tag_name, 'layers': layers, 'platforms': platforms, 'filters': filters})

def view_game(request, genre_id, game_id):
    return render(request, 'game/index.html', {'data': {'genre_id': genre_id, 'game_id': game_id, 'action': 'view_game'}})

class GameDetailView(DetailView):
    model = Game

    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()

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
        req_user = request.user
        
        if not req_tag_name == "":
            tag_name = text.slugify(req_tag_name)
            tag_game = Game.objects.get(id=game_id)

            # add new tag to db
            if not Tag.objects.filter(tag_name=tag_name, game=tag_game).exists():
                tag = Tag(tag_name=tag_name, popularity=1, game=tag_game)
                tag.save()
                tag.users.add(req_user)

            # increment popularity
            else:
                tag = Tag.objects.get(tag_name=tag_name, game=tag_game)
                if req_user not in tag.users.all():
                    tag.users.add(req_user)
                    tag.increment_popularity()
    
    # redirect to game page
    return redirect('game', genre_id=genre_id, pk=game_id)

def add_to_cart(request, genre_id, game_id):
    cart = request.user.profile.get_active_cart()
    cg = CartGamePurchase(game_id=game_id, cart_id=cart.id)
    cg.save()

    return redirect('game', genre_id=genre_id, pk=game_id)









