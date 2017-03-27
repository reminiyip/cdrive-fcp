from django.conf.urls import url, include

from . import views

browse_game_urls = [
    url(r'^homepage/', views.view_homepage, name='homepage'),
    url(r'^genre/(?P<genre_id>\d+)/$', views.view_genre, name='genre'),
    url(r'^genre/(?P<genre_id>\d+)/game/(?P<game_id>\d+)/$', views.view_game, name='game'), 
    url(r'^tag/(?P<tag_name>.+)', views.view_tagged_games, name='tagged_games'), 
]

review_urls = [
	url(r'^genre/(?P<genre_id>\d+)/game/(?P<game_id>\d+)/reviews/', views.view_reviews, name='reviews'), 
    url(r'^genre/(?P<genre_id>\d+)/game/(?P<game_id>\d+)/review/(?P<review_id>\d+)/$', views.view_review, name='review'),   
    url(r'^genre/(?P<genre_id>\d+)/game/(?P<game_id>\d+)/review/new/', views.new_review, name='new_review'),   
    url(r'^genre/(?P<genre_id>\d+)/game/(?P<game_id>\d+)/review/(?P<review_id>\d+)/edit/', views.edit_review, name='edit_review'),   
    url(r'^genre/(?P<genre_id>\d+)/game/(?P<game_id>\d+)/review/(?P<review_id>\d+)/remove/', views.remove_review, name='remove_review'), 
]

tag_urls = [
    url(r'^genre/(?P<genre_id>\d+)/game/(?P<game_id>\d+)/tag/(?P<tag_name>.+)/add/', views.add_tag, name='add_tag'),  
]

urlpatterns = browse_game_urls + review_urls + tag_urls