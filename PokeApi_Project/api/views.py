from django.shortcuts import render,redirect
from .forms import PokemonForm
from .models import Pokemon
from django.db.models import Q # Q object, se utiliza para construir consultas complejas y combinar condiciones en consultas en la DB
from django.core.exceptions import ObjectDoesNotExist # Excepcion para la view de editar y de enfrentamiento

# Create your views here.

def home(request): 
    return render(request, 'index.html') 

def create_pokemon(request): 
    if request.method == 'POST': # Cuando se llena el formulario va a ingresar al if porque hizo un request de metodo POST
        pokemon_form = PokemonForm(request.POST)
        print(pokemon_form.is_valid())
        if pokemon_form.is_valid():
            pokemon_form.save() # Metodo que tienen todos los modelos. Registra en la BD lo que se envio en el formulario
            return redirect('index') # Redirecciona a una URL
    else: # Es un GET. Cuando se ingrese la URL primero entra al else por ser un metodo GET y carga el formulario.
        pokemon_form = PokemonForm()
    pokemones = Pokemon.objects.all()
    #Listas con todas las coincidencias de cada campo sin repetir
    queryset = Pokemon.objects.values_list('nombre', flat=True)
    lista_nombre = list(set(queryset))
    queryset = Pokemon.objects.values_list('tipo', flat=True)
    lista_tipo = list(set(queryset))
    queryset = Pokemon.objects.values_list('naturaleza', flat=True)
    lista_naturaleza = list(set(queryset))
    queryset = Pokemon.objects.values_list('peso', flat=True)
    lista_peso = list(set(queryset))
    queryset = Pokemon.objects.values_list('ataque', flat=True)
    lista_ataque = list(set(queryset))
    return render(request, 'api/create_pokemon.html', {'pokemon_form': PokemonForm, 'pokemones':pokemones, 'lista_nombre':lista_nombre,
    'lista_tipo':lista_tipo,'lista_naturaleza':lista_naturaleza, 'lista_peso':lista_peso,'lista_ataque':lista_ataque}) 
    # Le manda la variable pokemon_form y pokemones al template

def filtrado(request, nombre_enlace, nombre_campo):
    pokemones_filtrados = Pokemon.objects.filter(**{nombre_campo: nombre_enlace})
    return render(request, 'api/filtrado.html', {'pokemones_filtrados':pokemones_filtrados, 'nombre_enlace':nombre_enlace, 'nombre_campo':nombre_campo})

def filtrado_busqueda(request):
    parametro_busqueda = request.GET.get('q', '') # Se obtiene el contenido de la busqueda, q es la key de la barra
    if (parametro_busqueda):
        pokemones_filtrados = Pokemon.objects.filter(Q(nombre__icontains=parametro_busqueda) | Q(tipo__icontains=parametro_busqueda) 
                                                     | Q(naturaleza__icontains=parametro_busqueda))
        return render(request, 'api/filtrado.html', {'pokemones_filtrados':pokemones_filtrados, 'nombre_campo':parametro_busqueda})
  
def edit_pokemon(request,id):
    error = None # Si no se inicializan y ocurre un error va a querer renderizar la plantilla con dos variables no creadas
    pokemon_form = None
    try:
        pokemon = Pokemon.objects.get(id = id) # Trae de la BD un unico resultado. Filter trae una lista
        if request.method == 'GET':
            pokemon_form = PokemonForm(instance = pokemon)
        else:
            pokemon_form = PokemonForm(request.POST, instance = pokemon)
            if pokemon_form.is_valid():
                pokemon_form.save()
            return redirect('index')
    except Exception as e:
        error = e 
    return render(request,'api/edit_pokemon.html', {'pokemon_form':pokemon_form, 'error':error, 'pokemon':pokemon})

def delete_pokemon(request,id):
    pokemon = Pokemon.objects.get(id = id)
    if request.method == 'POST':
        pokemon.delete()
        return redirect('api:create_pokemon')
    return render(request,'api/delete_pokemon.html', {'pokemon':pokemon})

def nemesis_pokemon(request,id):
        pokemon_filter = None
        error = None
        tipo = None
        debilidades = {
                'Normal': ['Lucha'],
                'Fuego': ['Agua', 'Tierra', 'Roca'],
                'Agua': ['Planta', 'Electrico'],
                'Planta': ['Fuego', 'Hielo', 'Veneno', 'Volador', 'Bicho'],
                'Electrico': ['Tierra'],
                'Hielo': ['Fuego', 'Lucha', 'Roca', 'Acero'],
                'Lucha': ['Volador', 'Psiquico', 'Hada'],
                'Veneno': ['Tierra', 'Psiquico'],
                'Tierra': ['Agua', 'Planta', 'Hielo'],
                'Volador': ['Electrico', 'Hielo', 'Roca'],
                'Psiquico': ['Bicho', 'Fantasma', 'Siniestro'],
                'Bicho': ['Volador', 'Roca', 'Fuego'],
                'Roca': ['Agua', 'Planta', 'Lucha', 'Tierra', 'Acero'],
                'Fantasma': ['Fantasma', 'Siniestro'],
                'Dragon': ['Hielo', 'Dragon', 'Hada'],
                'Siniestro': ['Lucha', 'Bicho', 'Hada'],
                'Acero': ['Fuego', 'Lucha', 'Tierra'],
                'Hada': ['Veneno', 'Acero']
            }
        try:
            pokemon = Pokemon.objects.get(id = id)
            tipo = pokemon.tipo
            pokemon_filter = Pokemon.objects.filter(tipo__in=debilidades[tipo])
        except Exception as e:
            error = e 
        return render(request, 'api/nemesis.html', {'pokemones':pokemon_filter, 'tipos':tipo, 'error':error})

def remove_pokemon(request):
    tipo_pokemon = request.GET.get('tipo') # Cuando se pasa el parametro ?tipo="tipo" se lo recupera
    pokemon = Pokemon.objects.filter(tipo = tipo_pokemon)
    if request.method == "POST":
        pokemon.delete()
        return redirect('api:create_pokemon')
    return render(request, 'api/remove_pokemon.html', {'tipo':tipo_pokemon})

def enfrentamiento(request):
    debilidades = {
            'Normal': ['Lucha'],
            'Fuego': ['Agua', 'Tierra', 'Roca'],
            'Agua': ['Planta', 'Eléctrico'],
            'Planta': ['Fuego', 'Hielo', 'Veneno', 'Volador', 'Bicho'],
            'Eléctrico': ['Tierra'],
            'Hielo': ['Fuego', 'Lucha', 'Roca', 'Acero'],
            'Lucha': ['Volador', 'Psíquico', 'Hada'],
            'Veneno': ['Tierra', 'Psíquico'],
            'Tierra': ['Agua', 'Planta', 'Hielo'],
            'Volador': ['Eléctrico', 'Hielo', 'Roca'],
            'Psíquico': ['Bicho', 'Fantasma', 'Siniestro'],
            'Bicho': ['Volador', 'Roca', 'Fuego'],
            'Roca': ['Agua', 'Planta', 'Lucha', 'Tierra', 'Acero'],
            'Fantasma': ['Fantasma', 'Siniestro'],
            'Dragón': ['Hielo', 'Dragón', 'Hada'],
            'Siniestro': ['Lucha', 'Bicho', 'Hada'],
            'Acero': ['Fuego', 'Lucha', 'Tierra'],
            'Hada': ['Veneno', 'Acero']
        }
    ganador = False
    error = None 
    if request.method == "POST":
        form_data = request.POST
      
    
        try:
            id_contendiente = form_data['pokemon_contendiente']
            id_contrincante = form_data['pokemon_contrincante']
            pokemon_contrincante = Pokemon.objects.get(id = id_contrincante)
            pokemon_contendiente = Pokemon.objects.get(id = id_contendiente)
            if(pokemon_contendiente.tipo in debilidades.get(pokemon_contrincante.tipo, [])):
                ganador = True
            return render(request, 'api/ganador.html', {'ganador':ganador, 'contrincante':pokemon_contrincante, 'contendiente':pokemon_contendiente})
        except Exception as e:
            error = e 
        
    return render(request,'api/enfrentamiento.html', {'ganador':ganador, 'error':error})

