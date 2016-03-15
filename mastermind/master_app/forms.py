from django import forms

class NewGameForm(forms.Form):
   player_name = forms.CharField(label='Player Name', max_length=100)

   