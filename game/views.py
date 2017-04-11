from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.utils import timezone, text
from django.urls import reverse
from collections import OrderedDict

from .models import Game, Genre, Tag, Platform, Review
from core.models import Cart, CartGamePurchase
from django.contrib.auth.models import User
from cdrive_fcp.utils.utils import HelperUtils
from cdrive_fcp.utils.const import GameConst

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ReviewForm, ReviewDeleteForm
from django.contrib import messages

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
    genre_groups = HelperUtils.get_column_groups(genres, num_of_cols=4)
    
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
    featured_game_groups = HelperUtils.get_column_groups(featured_games, num_of_cols=3)

    # layers
    layers = {'Home': '#'}

    return render(request, 'game/homepage.html', {'genres': genre_groups, 'recommendations': recommended_games, 'featured_games': featured_game_groups, 'layers': layers})

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
    game = Game.objects.get(pk=game_id)

    review_list = Review.objects.filter(game=game_id).order_by('-review_issue_date')
    review_groups = HelperUtils.get_column_groups(review_list)
    paginator = Paginator(review_groups, 5) # show 10 reviews per page, i.e. 5 rows

    # form page_header dict
    layers = OrderedDict()
    layers['Home'] = reverse('homepage')
    layers[game.genre.genre_name] = reverse('genre', args=[game.genre.id])
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

def add_review(request, genre_id, game_id):
    game = Game.objects.get(pk=game_id)

    if request.user.is_authenticated() and game in request.user.profile.get_purchased_games():
        if request.method == 'POST':
            form = ReviewForm(request.POST)

            if form.is_valid():

                review = form.save(commit=False)
                review.review_issue_date = timezone.now()
                review.user = request.user
                review.game = game
                review.save()
                return redirect('reviews', genre_id=game.genre.id, game_id=game.id)
        else:
            form = ReviewForm()

            # form page_header dict
            layers = OrderedDict()
            layers['Home'] = reverse('homepage')
            layers[game.genre.genre_name] = reverse('genre', args=[game.genre.id])
            layers[game.title] = reverse('game', kwargs={'genre_id': game.genre.id, 'pk': game.id})
            layers['Review'] = '#'
            page  = request.GET.get('page')

        return render(request, 'game/add_review.html', {'game': game,'form': form, 'layers': layers})
    else:
        return redirect('login')

def edit_review(request, genre_id, game_id, review_id):
    review = Review.objects.get(pk=review_id)
    game = Game.objects.get(pk=game_id)

    if request.user.is_authenticated() and review in request.user.profile.get_posted_reviews():
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
            layers[game.genre.genre_name] = reverse('genre', args=[game.genre.id])
            layers[game.title] = reverse('game', kwargs={'genre_id': game.genre.id, 'pk': game.id})
            layers['Review'] = '#'
            page  = request.GET.get('page')

        return render(request, 'game/edit_review.html', {'game': game, 'form': form, 'layers': layers})
    else:
        return redirect('login')

def delete_review(request, genre_id, game_id, review_id):
    review = Review.objects.get(pk=review_id)
    game = Game.objects.get(pk=game_id)

    if request.user.is_authenticated() and review.user == request.user:

        if request.method == "POST":
            form = ReviewDeleteForm(request.POST, instance=review)

            if form.is_valid():
                review.delete()
                return redirect('reviews', genre_id=game.genre.id, game_id=game.id)
        else:
            form = ReviewDeleteForm(instance=review)

            # form page_header dict
            layers = OrderedDict()
            layers['Home'] = reverse('homepage')
            layers[game.genre.genre_name] = reverse('genre', args=[game.genre.id])
            layers[game.title] = reverse('game', kwargs={'genre_id': game.genre.id, 'pk': game.id})
            layers['Review'] = '#'
            page  = request.GET.get('page')

        return render(request, 'game/delete_review.html', {'game': game, 'form': form, 'layers': layers})
        
    else:
        return redirect('login')


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