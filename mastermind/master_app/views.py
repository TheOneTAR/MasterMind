from django.shortcuts import render

# Create your views here.

def landing_page(request):
   '''Landing page VC for the Mastermind app game.'''
   return render(request, 'master_app/index.html')