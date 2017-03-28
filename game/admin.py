from django.contrib import admin

from .models import Genre, Game, Review, Tag, Platform

admin.site.register(Genre) 
admin.site.register(Game) 
admin.site.register(Review)
admin.site.register(Tag)
admin.site.register(Platform)
