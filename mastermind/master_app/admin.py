from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(KeyPeg)
admin.site.register(ColorPeg)
admin.site.register(Code)
admin.site.register(Game)
admin.site.register(Guess)