from django.conf.urls import url
from .views import *

urlpatterns = [
   url(r'^newGame', create_new_game, name='new_game'),
   url(r'^game/newGuess', submit_guess, name='new_guess'),
   url(r'^game/(?P<game_id>[0-9]+)', game, name='game'),
   url(r'^$', landing_page),

]