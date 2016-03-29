from django.db import models
import random

# Create your models here.

class KeyPeg(models.Model):
   '''
   The KeyPeg class defines the structure for the
   Mastermind's replies to the Decoder.
   '''
   BLACK = 0
   WHITE = 1

   Color = (
      (BLACK, 'black'),
      (WHITE, 'white')
   )

   color = models.IntegerField(choices=Color, default=BLACK)
   guess_id = models.ForeignKey('Guess')

   def __str__(self):
      return self.Color[self.color][1]

class ColorPeg(models.Model):
   '''
   The core component of a game of Mastermind: the color peg.
   '''

   # Possibly colors of the pegs
   BLUE = 0
   WHITE = 1
   RED = 2
   GREEN = 3
   BLACK = 4
   YELLOW = 5
   PURPLE = 6

   Color = (
      (BLUE, 'blue'),
      (WHITE, 'white'),
      (RED, 'red'),
      (GREEN, 'green'),
      (BLACK, 'black'),
      (YELLOW, 'yellow'),
      (PURPLE, 'purple')
   )

   color = models.IntegerField(choices=Color, default=BLUE)

   def __str__(self):
      return self.Color[self.color][1]


class GameType(models.Model):
   '''Allows there to be multiple types of games.
      Kids game has 3 pegs,
      Normal has 4, 
      Hard has 5, etc.
   '''

   num_pegs = models.PositiveSmallIntegerField()
   num_colors = models.PositiveSmallIntegerField(default=6)
   name = models.CharField(max_length=100)
   description = models.TextField(max_length=600)

   def __str__(self):
      return self.name


class GameManager(models.Manager):
   '''
   Manager for the Game object. Generates the secret code,
   and allows passing in of the player's name on creation.
   '''

   def create_game(self, name, game_type):
      '''
      Create a game with a new code and given player name.
      Call by using 'Book.objects.create_game(player_name)'
      '''

      game = self.create(player_name=name, game_type=game_type)

      num = game_type.num_pegs
      color_num = game_type.num_colors

      # Loop through and randomly generate a code of num_pages length
      for i in range(1, num+1):
         color = random.choice(ColorPeg.objects.all()[:color_num])
         CodePeg.objects.create(color=color, game=game, slot_num=i)

      return game

      

class Game(models.Model):
   '''
   The game itself. Stores the game id etc.
   '''

   # Status Consts
   GAME_OVER = 0
   PLAYING = 1
   WINNER = 2

   Status = (
      (GAME_OVER, 'Game Over :('),
      (PLAYING, 'In Progress'),
      (WINNER, 'You Won!')
   )

   player_name = models.CharField(max_length=100)
   status = models.IntegerField(choices=Status, default=PLAYING)
   code = models.ManyToManyField(ColorPeg, through='CodePeg')
   game_type = models.ForeignKey(GameType) 

   objects = GameManager()

   def __str__(self):
      return self.player_name + "'s game"

   def status_str(self):
      return self.Status[self.status][1]

class CodePeg(models.Model):
   '''Table that establishes the code of the master per every game.'''

   game = models.ForeignKey(Game)
   color = models.ForeignKey(ColorPeg)
   slot_num = models.PositiveSmallIntegerField()

   def __str__(self):
      return "Game " + str(self.game.pk) + " Slot " + str(self.slot_num) + " Color " + str(self.color.pk)

class Guess(models.Model):
   '''
   A Decoder's single Guess, associated with a game and 
   with what number it is.
   '''
   # The four slots of what the user is guessing
   # Why do you even need this?
   slots = models.ManyToManyField(ColorPeg, through='GuessPeg')

   # Which guess it is
   num = models.IntegerField()

   # Game the Guess is associated with
   game_id = models.ForeignKey(Game)

   def __str__(self):
      return "Guess " + str(self.num) + " for Game " + str(self.game_id.pk)

class GuessPeg(models.Model):
   '''Table that establishes the guess of the user per every game.'''

   guess = models.ForeignKey(Guess)
   color_id = models.ForeignKey(ColorPeg)
   slot_num = models.PositiveSmallIntegerField()

   class Meta:
      ordering = ['slot_num']


   def __str__(self):
      return str(self.color_id) + " in slot " + str(self.slot_num)

