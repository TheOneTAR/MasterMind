from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

import json

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

   # Get the number of pegs in each guess
   num_slots = range(1, game.game_type.num_pegs+1)

   # Get the colors used in this game for making guesses
   colors = get_colors(game)

   # Get the key color defaults
   key_color = KeyPeg.Color

   # Get the master code.
   # TODO: This isn't needed until the game is over.
   code = []

   for peg in game.code.all():
      code.append(ColorPeg.Color[peg.color][1])

   # Get the guesses assoicated with a game
   #  Setup the guess pegs and keypegs for each guess
   try: 
      db_guesses = Guess.objects.filter(game_id=game)
      guesses = []

      for guess in db_guesses:
         pegs = []
         keys = []
         for peg in guess.guesspeg_set.all():
            pegs.append({'color': ColorPeg.Color[peg.color_id.color][1], 'num': peg.slot_num})

         for key in guess.keypeg_set.all():
            keys.append(key_color[key.color][1])

         guesses.append({'keys': keys, 'pegs':pegs})
   except ObjectDoesNotExist:
      guesses = []

   return render(
         request,
         'master_app/game.html', 
         {
            'game': game,
            'code':code,
            'guesses': guesses,
            'num_slots': num_slots,
            'colors': colors,
            'curr_guess': len(guesses) + 1
         })


def get_colors(game):
   '''Get the colors associated with a given game.'''

   # game_type has num_colors, which can be used to slice from Colors list.
   color_num = game.game_type.num_colors
   colors_in_game = ColorPeg.objects.all()[:color_num]

   colors = []
   for color in colors_in_game:
      color.name = ColorPeg.Color[color.color][1]
      colors.append(color)

   return colors

def submit_guess(request):

   if request.method == 'POST':
      print('SUCCESS')
      json_data = request.POST.get('the_data')
      data = json.loads(json_data)

      # Get the game id and game
      game_id = data[1]['value']
      game = Game.objects.get(pk=game_id)

      # Get the master code for this game
      code = {}

      for peg in game.codepeg_set.all():
         code[peg.slot_num] = peg.color.pk

      # Get the guess number
      guess_num = data[2]['value']

      # Make a new Guess
      guess = Guess(
            game_id = game,
            num = guess_num
         )

      guess.save()

      guess_id = guess.pk

      guess_dict = {}

      # Loop through the rest of the array to get the slot stuff
      for slot in data[3:]:
         slot_num = slot['name']
         slot_color_id = slot['value']

         guess_dict[int(slot_num)] = int(slot_color_id)

         color_peg = ColorPeg.objects.get(pk=slot_color_id)

         # Build a GuessPeg associated with the game for that peg and slot
         peg = GuessPeg(guess=guess, color_id=color_peg, slot_num=slot_num)
         peg.save()

      # Evaluate if the guess is correct for this peg
      eval_guess(code, guess_dict, len(data[3:]), guess)



   return JsonResponse({'foo':'bar'})


def eval_guess(code, guess, num_slots, guess_obj):
   print("code:",code, "guess:", guess)

   # Using the algorithm that Ron and Sarah came up with,
   # but tweaked for my implentation

   # First look for exact matches
   for peg in range(1, num_slots+1):
      if code[peg] == guess[peg]:
         
         # Black peg!
         black_peg = KeyPeg(guess_id=guess_obj, color=KeyPeg.BLACK)
         black_peg.save()

         code[peg] = ""
         guess[peg] = ""

   # Then look for color matches
   for peg in range(1, num_slots+1):
      if guess[peg] != "":
         for in_peg in range(1, num_slots+1):
            if code[in_peg] != "":
               if guess[peg] == code[in_peg]:

                  #White Peg!!
                  white_peg = KeyPeg(guess_id=guess_obj, color=KeyPeg.WHITE)
                  white_peg.save()

                  code[in_peg] == ""
                  break










