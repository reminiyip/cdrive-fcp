from __future__ import unicode_literals
from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    genre_name = models.CharField(max_length=30)

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
    
    def add_to_genre(self, genre_id):
        return

class Review(models.Model):
    review_header = models.CharField(max_length=50)
    review_content = models.TextField()
    review_issue_date = models.DateField()
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
