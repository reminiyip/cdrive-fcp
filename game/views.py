from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.utils import timezone, text
from django.urls import reverse
from collections import OrderedDict

from .models import Game, Genre, Tag, Platform, Review
from core.models import Cart, CartGamePurchase
from django.contrib.auth.models import User
from cdrive_fcp.utils.const import GameConst
from cdrive_fcp.decorators import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ReviewForm, ReviewDeleteForm
from django.contrib import messages


##############################################################################
#                                    browse games                            #
##############################################################################

def homepage(request):
    genres = Genre.objects.all()
    
    # recommendations
    if request.user.is_authenticated:
        purchased_games = request.user.profile.get_purchased_games()

        num_of_targets = min(GameConst.NUM_OF_TARGETS_FOR_RECOMMENDATION, purchased_games.count())
        targets = purchased_games[:num_of_targets]

        recommended_games = []
        for target in targets:
            game = target.get_most_similar_game(user=request.user)
            if game is not None and game not in recommended_games:
                recommended_games.append(game)
    else:
        recommended_games = None

    # featured games
    featured_games = Game.objects.filter(is_featured=True)

    # layers
    layers = {'Home': '#'}

    return render(request, 'game/homepage.html', {'genres': genres, 'recommendations': recommended_games, 'featured_games': featured_games, 'layers': layers})

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
            filters = platforms.values_list('name', flat=True)
        context['filters'] = filters

        # get sorted games, group by 2
        games = Game.objects.filter(genre_id=context['genre'].id, platforms__name__in=filters).distinct().order_by('-release_date')
        context['games'] = games

        # form page_header dict
        layers = OrderedDict()
        layers['Home'] = reverse('homepage')
        layers[context['genre'].name] = '#'
        context['layers'] = layers

        return context

def tagged_games(request, tag_name):
    # platforms
    platforms = Platform.objects.all()

    # get filters
    if request.GET.get('filters') != None:
        filters = request.GET.get('filters').split(',')
    else:
        filters = platforms.values_list('name', flat=True)

    # games
    games = Game.objects.filter(tag__name__contains=tag_name, platforms__name__in=filters).distinct().order_by('-release_date')

    # form page_header dict
    layers = OrderedDict()
    layers['Home'] = reverse('homepage')
    layers['Tag - {}'.format(tag_name)] = '#'

    return render(request, 'game/tag.html', {'games': games, 'tag_name': tag_name, 'layers': layers, 'platforms': platforms, 'filters': filters})

@method_decorator(genre_is_valid, name="dispatch")
class GameDetailView(DetailView):
    model = Game

    def dispatch(self, *args, **kwargs):
        return super(GameDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()

        # form page_header dict
        layers = OrderedDict()
        layers['Home'] = reverse('homepage')
        layers[context['game'].genre.name] = reverse('genre', args=[context['game'].genre.id])
        layers[context['game'].title] = '#'
        context['layers'] = layers

        return context

##############################################################################
#                                 game review actions                        #
##############################################################################

@genre_is_valid
@game_is_valid
def view_reviews(request, genre_id, game_id):
    
    genre = Genre.objects.get(pk=genre_id)
    game = Game.objects.get(pk=game_id)

    review_list = Review.objects.filter(game=game_id).order_by('-issue_date')
    paginator = Paginator(review_list, 5) # show 5 reviews per page

    # form page_header dict
    layers = OrderedDict()
    layers['Home'] = reverse('homepage')
    layers[game.genre.name] = reverse('genre', args=[game.genre.id])
    layers[game.title] = reverse('game', kwargs={'genre_id': game.genre.id, 'pk': game.id})
    layers['Review'] = '#'

    page  = request.GET.get('page')

    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)

    return render(request, 'game/review.html', {'reviews': reviews, 'game': game, 'layers': layers})

@login_required
@genre_is_valid
@game_is_valid
@user_purchased_the_game
def add_review(request, genre_id, game_id):
    game = Game.objects.get(pk=game_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)
            review.issue_date = timezone.now()
            review.user = request.user
            review.game = game
            review.save()
            return redirect('reviews', genre_id=game.genre.id, game_id=game.id)
    else:
        form = ReviewForm()

        # form page_header dict
        layers = OrderedDict()
        layers['Home'] = reverse('homepage')
        layers[game.genre.name] = reverse('genre', args=[game.genre.id])
        layers[game.title] = reverse('game', kwargs={'genre_id': game.genre.id, 'pk': game.id})
        layers['Review'] = '#'
        page  = request.GET.get('page')

    return render(request, 'game/add_review.html', {'game': game,'form': form, 'layers': layers})

@login_required
@genre_is_valid
@game_is_valid
@user_posted_the_review
def edit_review(request, genre_id, game_id, review_id):
    review = Review.objects.get(pk=review_id)
    game = Game.objects.get(pk=game_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            form.save()
            return redirect('reviews', genre_id=game.genre.id, game_id=game.id)

        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ReviewForm(instance=review, label_suffix='')

        # form page_header dict
        layers = OrderedDict()
        layers['Home'] = reverse('homepage')
        layers[game.genre.name] = reverse('genre', args=[game.genre.id])
        layers[game.title] = reverse('game', kwargs={'genre_id': game.genre.id, 'pk': game.id})
        layers['Review'] = '#'
        page  = request.GET.get('page')
    return render(request, 'game/edit_review.html', {'game': game, 'form': form, 'review': review, 'layers': layers})

# keep the confirmation page, one-click deletion may cause unfriendly experience
@login_required
@genre_is_valid
@game_is_valid
@user_posted_the_review
def delete_review(request, genre_id, game_id, review_id):
    review = Review.objects.get(pk=review_id)
    game = Game.objects.get(pk=game_id)

    if request.method == 'POST':
        form = ReviewDeleteForm(request.POST, instance=review)

        if form.is_valid():
            review.delete()
            return redirect('reviews', genre_id=genre_id, game_id=game_id)
    else:
        form = ReviewDeleteForm(instance=review)

        # form page_header dict
        layers = OrderedDict()
        layers['Home'] = reverse('homepage')
        layers[game.genre.name] = reverse('genre', args=[game.genre.id])
        layers[game.title] = reverse('game', kwargs={'genre_id': game.genre.id, 'pk': game.id})
        layers['Review'] = '#'
        page  = request.GET.get('page')
    return render(request, 'game/delete_review.html', {'game': game, 'form': form, 'review': review, 'layers': layers})


##############################################################################
#                                      actions                               #
##############################################################################

@login_required
@genre_is_valid
@game_is_valid
@user_purchased_the_game
def add_tag(request, genre_id, game_id):
    if request.method == 'POST':
        req_tag_name = request.POST.get('tag_name', None)
        req_user = request.user
        
        if not req_tag_name == "":
            tag_name = text.slugify(req_tag_name)
            tag_game = Game.objects.get(id=game_id)

            # add new tag to db
            if not Tag.objects.filter(name=tag_name, game=tag_game).exists():
                tag = Tag(name=tag_name, popularity=1, game=tag_game)
                tag.save()
                tag.users.add(req_user)

            # increment popularity
            else:
                tag = Tag.objects.get(name=tag_name, game=tag_game)
                if req_user not in tag.users.all():
                    tag.users.add(req_user)
                    tag.increment_popularity()
    
    # redirect to game page
    return redirect('game', genre_id=genre_id, pk=game_id)

@login_required
@genre_is_valid
@game_is_valid
@user_not_purchased_the_game_and_game_not_in_active_cart
def add_to_cart(request, genre_id, game_id):
    cart = request.user.profile.get_active_cart()
    cg = CartGamePurchase(game_id=game_id, cart_id=cart.id)
    cg.save()

    return redirect('game', genre_id=genre_id, pk=game_id)