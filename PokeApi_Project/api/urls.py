from django.urls import path
from .views import create_pokemon, filtrado, filtrado_busqueda, edit_pokemon, delete_pokemon, nemesis_pokemon, remove_pokemon, enfrentamiento

urlpatterns = [
    path('pokemon/', create_pokemon, name = "create_pokemon"),
    path('enlace/<str:nombre_enlace>/<str:nombre_campo>/', filtrado, name = 'filtrado'),
    path('busqueda/', filtrado_busqueda, name = 'filtrado_search'),
    path('pokemon/<int:id>/', edit_pokemon , name = 'edit_pokemon'),
    path('pokemon/delete/<int:id>', delete_pokemon, name = 'delete_pokemon'),
    path('nemesis/<int:id>', nemesis_pokemon, name = 'nemesis_pokemon'),
    path('remove-tipo/', remove_pokemon, name = 'remove_pokemon'),
    path('enfrentamiento/', enfrentamiento, name = 'enfrentamiento_pokemon'),
    
    
]