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
      (BLACK, 'Black'),
      (WHITE, 'White')
   )

   color = models.IntegerField(choices=Color, default=BLACK)

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

   Color = (
      (BLUE, 'Blue'),
      (WHITE, 'White'),
      (RED, 'Red'),
      (GREEN, 'Green'),
      (BLACK, 'Black'),
      (YELLOW, 'Yellow')
   )

   color = models.IntegerField(choices=Color, default=BLUE)

   def __str__(self):
      return self.Color[self.color][1]

class Code(models.Model):
   '''
   A Mastermind's code.
   '''
   # The four slots of what the user is guessing
   slot_1 = models.ForeignKey(ColorPeg, related_name='code_1')
   slot_2 = models.ForeignKey(ColorPeg, related_name='code_2')
   slot_3 = models.ForeignKey(ColorPeg, related_name='code_3')
   slot_4 = models.ForeignKey(ColorPeg, related_name='code_4')

   def __str__(self):
      '''Represent the guess as the color pattern'''
      return str(self.slot_1) + " " + str(self.slot_2) + " " + str(self.slot_3) + " " + str(self.slot_4)

class GameManager(models.Manager):
   '''
   Manager for the Game object. Generates the secret code,
   and allows passing in of the player's name on creation.
   '''

   def create_game(self, name):
      '''
      Create a game with a new code and given player name.
      Call by using 'Book.objects.create_game(player_name)'
      '''

      code = self.generate_code()
      game = self.create(player_name=name, code=code)

      return game

   def generate_code(self):
      '''
      Randomly generate a 4 ColorPeg code and return it.
      '''
      code = Code()
      code.slot_1 = random.choice(ColorPeg.objects.all())
      code.slot_2 = random.choice(ColorPeg.objects.all())
      code.slot_3 = random.choice(ColorPeg.objects.all())
      code.slot_4 = random.choice(ColorPeg.objects.all())

      code.save()
      return code


class Game(models.Model):
   '''
   The game itself. Stores the game id etc.
   '''

   # Status Consts
   GAME_OVER = 0
   PLAYING = 1

   Status = (
      (GAME_OVER, 'Game Over'),
      (PLAYING, 'In Progress')
   )

   player_name = models.CharField(max_length=100)
   status = models.IntegerField(choices=Status, default=PLAYING)
   code = models.ForeignKey(Code, null=True, blank=True)

   objects = GameManager()

   def __str__(self):
      return self.player_name + "'s " + self.status_str() + " game"

   def status_str(self):
      return self.Status[self.status][1]

class Guess(models.Model):
   '''
   A Decoder's single Guess, associated with a game and 
   with what number it is.
   '''
   # The four slots of what the user is guessing
   slot_1 = models.ForeignKey(ColorPeg, related_name='slot_1')
   slot_2 = models.ForeignKey(ColorPeg, related_name='slot_2')
   slot_3 = models.ForeignKey(ColorPeg, related_name='slot_3')
   slot_4 = models.ForeignKey(ColorPeg, related_name='slot_4')

   # Replies to the guess
   key_1 = models.ForeignKey(KeyPeg, related_name='key_1', null=True, blank=True)
   key_2 = models.ForeignKey(KeyPeg, related_name='key_2', null=True, blank=True)
   key_3 = models.ForeignKey(KeyPeg, related_name='key_3', null=True, blank=True)
   key_4 = models.ForeignKey(KeyPeg, related_name='key_4', null=True, blank=True)

   # Which guess it is
   num = models.IntegerField()

   # Game the Guess is associated with
   game_id = models.ForeignKey(Game)

   def __str__(self):
      '''Represent the guess as the color pattern'''
      return str(self.slot_1) + " " + str(self.slot_2) + " " + str(self.slot_3) + " " + str(self.slot_4)

