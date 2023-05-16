from django.contrib import admin
from .models import Pokemon
# Register your models here.

class PokemonAdmin(admin.ModelAdmin):
    list_display=('nombre','tipo','naturaleza','peso','ataque')

admin.site.register(Pokemon,PokemonAdmin)