from django.contrib import admin

from .models import Genre, Game, Review, Tag

admin.site.register(Genre) 
admin.site.register(Game) 
admin.site.register(Review)
admin.site.register(Tag)
