from __future__ import unicode_literals
from decimal import Decimal
from django.db.models import Count

from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

class Genre(models.Model):
    genre_name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='genres')

    def __str__(self):
        return self.genre_name

class Game(models.Model):
    image = models.ImageField(upload_to='games')
    title = models.CharField(max_length=50)
    full_description = models.TextField()
    one_line_description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    is_featured = models.BooleanField()
    platforms = models.ManyToManyField('Platform')
    release_date = models.DateField()
        
    def __str__(self):
        return self.title

    def get_sorted_tags(self):
        tags = Tag.objects.filter(game_id=self.id).order_by('-popularity')
        return tags
    
    def get_similar_games(self, filter_purchased=True, user=None):
        # get all tag names related to this game
        tag_names = self.get_sorted_tags().values_list('tag_name', flat=True)

        # get games to check similarity, based on whether to filter purchased history or not
        if filter_purchased and user is not None:
            purchased_games_id = user.profile.get_purchased_games_id()
            games = Game.objects.exclude(pk__in=set(purchased_games_id)).order_by('-release_date')
        else:
            games = Game.objects.all().order_by('-release_date')

        # annotate similarity
        similar_games = games.filter(tag__tag_name__in=tag_names).annotate(similarity=Count('tag')).order_by('-similarity')

        return similar_games

    def get_most_similar_game(self, filter_purchased=True, user=None):
        games = self.get_similar_games(filter_purchased=filter_purchased, user=user)
        return games[0] if games.count() else None
            
    def add_to_genre(self, genre_id):
        return

class Review(models.Model):
    review_header = models.CharField(max_length=50)
    review_content = models.TextField()
    review_issue_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)

    def __str__(self):
        return "{}: {}".format(self.user.username, self.game.title)

class Tag(models.Model):
    tag_name = models.CharField(max_length=30)
    popularity = models.PositiveIntegerField()
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    users = models.ManyToManyField(User)
    
    def __str__(self):
        return self.tag_name

    def increment_popularity(self):
        self.popularity += 1
        self.save()

class Platform(models.Model):
    WINDOWS = 'W'
    MAC = 'M'
    LINUX = 'L'
    PLATFORM_CHOICES = (
        (WINDOWS, 'Windows'),
        (MAC, 'MacOS'),
        (LINUX, 'Linux'),
    )
    LOGO_CHOICES = {
        WINDOWS: '/static/img/logos/windows-logo.png',
        MAC: '/static/img/logos/apple-logo.png',
        LINUX: '/static/img/logos/linux-logo.png',
    }
    platform_name = models.CharField(max_length=2, choices=PLATFORM_CHOICES, primary_key=True, default=WINDOWS) 

    def __str__(self):
        return self.get_platform_name_display()

    def get_logo_path(self):
        return Platform.LOGO_CHOICES[self.platform_name]
