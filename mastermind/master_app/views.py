from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

from .models import *
from .forms import * 

# Create your views here.

def landing_page(request):
   '''Landing page VC for the Mastermind app game.'''

   types = GameType.objects.all()

   return render(request, 'master_app/index.html', {'types':types})

def create_new_game(request):

   if request.method == 'POST':
      form = NewGameForm(request.POST)
      if form.is_valid():

         name = form.cleaned_data['player_name']
         game_type = form.cleaned_data['game_type']

         # To test things, make a new game
         game = Game.objects.create_game(name, game_type)

         return HttpResponseRedirect('/game/' + str(game.id))

   return render(request, 'master_app/index.html')

def game(request, game_id):

   game = Game.objects.get(pk=game_id)

   colors = ColorPeg.Color
   key_color = KeyPeg.Color

   code = []

   for peg in game.code.all():
      code.append(colors[peg.color][1])

   # Get the guesses assoicated with a game
   #  Setup the guess pegs and keypegs for each guess
   try: 
      db_guesses = Guess.objects.filter(game_id=game)
      print(db_guesses)
      guesses = []

      for guess in db_guesses:
         print(guess)
         pegs = []
         keys = []
         for peg in guess.slots.all():
            print(peg)
            pegs.append(colors[peg.color][1])

         for key in guess.keys.all():
            keys.append(key_color[key.color][1])

         guesses.append({'keys': keys, 'pegs':pegs})
   except ObjectDoesNotExist:
      guesses = []

   return render(request, 'master_app/game.html', {'game': game, 'code':code, 'guesses': guesses})





