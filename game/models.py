from __future__ import unicode_literals

from django.db import models

# Create your models here.

Class Game

    game_id = models.PositiveIntegerField()
    image = models.ImageField()
    title = models.CharField(max_length=30)
    full_description = models.TextField()
    one_line_description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    platform = models.ManyToManyField(Platform)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)
    is_featured = models.BooleanField()
    
    def make_new_tag(self,Tag):
        
    def delete_tag(self,Tag):
        
    def make_new_review(self,User, Review):
        
    def delete_review(self,User, Review):
        
    def edit_review(self,User, Review):
        
    def get_sorted_tags(self)
    
    def add_to_genre(self,Genre)


Class Review

    review_id = models.PositiveIntegerField()
    review_header = models.CharField(max_length=50)
    review_content = models.TextField()
    review_issue_date = models.DateField()
    user_name = models.CharField()
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    

Class Platform

    platform_id = models.PositiveIntegerField()
    platform_name = models.CharField(max_length=20)
    

Class Genre
    genre_id = models.PositiveIntegerField()
    genre_name = models.CharField(max_length=30)

Class Tag
    tag_id = models.PositiveIntegerField()
    tag_name = models.CharField(max_length=30)
    popularity = models.PositiveIntegerField()
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    
    def increment_popularity(self):
        self.popularity += 1
        self.save()
