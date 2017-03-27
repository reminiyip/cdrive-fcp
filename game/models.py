from __future__ import unicode_literals

from django.db import models

# Create your models here.

Class Game

    game_id = 
    image = models.ImageField()
    title
    full_description
    one_line_description
    price = 
    reviews
    tags
    platform
    genre
    is_featured = models.BooleanField()
    
    def make_new_tag(self,Tag):
        
    def delete_tag(self,Tag):
        
    def make_new_review(self,User, Review):
        
    def delete_review(self,User, Review):
        
    def edit_review(self,User, Review):
        
    def get_sorted_tags(self)
    
    def add_to_genre(self,Genre)


Class Review

    review_id = models.
    review_header
    review_content
    review_issue_date
    user_name


Class Platform

    platform_id
    platform_name
    

Class Genre
    genre_id
    genre_name
    games

Class Tag
    tag_id
    tag_name
    popularity
    game_id
    
    def increment_popularity(self):
        self.popularity += 1
        self.save()
