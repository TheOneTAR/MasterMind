from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
from .forms import * 

# Create your views here.

def landing_page(request):
   '''Landing page VC for the Mastermind app game.'''

   return render(request, 'master_app/index.html')

def create_new_game(request):

   if request.method == 'POST':
      form = NewGameForm(request.POST)
      if form.is_valid():

         name = form.cleaned_data['player_name']

         # To test things, make a new game
         game = Game.objects.create_game(name)

         return HttpResponseRedirect('/game/' + str(game.id))

   return render(request, 'master_app/index.html')

def game(request, game_id):

   return render(request, 'master_app/game.html', {'id':game_id})