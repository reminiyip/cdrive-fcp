from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from decimal import Decimal

class Genre(models.Model):
    genre_name = models.CharField(max_length=30)

class Game(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=50)
    full_description = models.TextField()
    one_line_description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    is_featured = models.BooleanField()
    platform = models.ManyToManyField('Platform')
        
    def get_sorted_tags(self):
        return
    
    def add_to_genre(self, genre_id):
        return

class Review(models.Model):
    review_header = models.CharField(max_length=50)
    review_content = models.TextField()
    review_issue_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)

class Tag(models.Model):
    tag_name = models.CharField(max_length=30)
    popularity = models.PositiveIntegerField()
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    
    def increment_popularity(self):
        self.popularity += 1
        self.save()

class Platform(models.Model):
    PLATFORM_CHOICES = (
        ('W', 'Windows'),
        ('M', 'MacOS'),
        ('L', 'Linux'),
    )
    platform_name = models.CharField(max_length=2, choices=PLATFORM_CHOICES, primary_key=True, default='W') 
