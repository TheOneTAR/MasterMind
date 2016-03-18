from django import forms
from .models import GameType

class NewGameForm(forms.Form):
   player_name = forms.CharField(label='Player Name', max_length=100)
   game_type = forms.ModelChoiceField(queryset=GameType.objects.all())

   