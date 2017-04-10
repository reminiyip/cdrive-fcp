from django.conf.urls import url, include

from . import views
from .views import GameDetailView, GenreDetailView

browse_game_urls = [
    url(r'^homepage/', views.homepage, name='homepage'),
    url(r'^genre/(?P<pk>\d+)/$', GenreDetailView.as_view(), name='genre'),
    url(r'^genre/(?P<genre_id>\d+)/game/(?P<pk>\d+)/$', GameDetailView.as_view(), name='game'),
    url(r'^genre/(?P<genre_id>\d+)/game/(?P<game_id>\d+)/add_to_cart/$', views.add_to_cart, name='add_to_cart'), 
    url(r'^tag/(?P<tag_name>.+)', views.tagged_games, name='tagged_games'), 
]

review_urls = [
    url(r'^genre/(?P<genre_id>\d+)/game/(?P<game_id>\d+)/reviews/', views.view_reviews, name='reviews'),
    url(r'^genre/(?P<genre_id>\d+)/game/(?P<game_id>\d+)/add_review/', views.add_review, name='add_review'),
    url(r'^genre/(?P<genre_id>\d+)/game/(?P<game_id>\d+)/edit_review/(?P<review_id>\d+)/', views.edit_review, name='edit_review'),   
    url(r'^genre/(?P<genre_id>\d+)/game/(?P<game_id>\d+)/delete_review/(?P<review_id>\d+)/', views.delete_review, name='delete_review'), 
]

tag_urls = [
    #url(r'^genre/(?P<genre_id>\d+)/game/(?P<game_id>\d+)/tag/(?P<tag_name>.+)/add/', views.add_tag, name='add_tag'), 
    url(r'^genre/(?P<genre_id>\d+)/game/(?P<game_id>\d+)/tag/add/', views.add_tag, name='add_tag'),
]

urlpatterns = browse_game_urls + review_urls + tag_urls