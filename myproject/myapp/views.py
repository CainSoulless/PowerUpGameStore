from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .src.login.forms import RegistroForm 
from django.contrib import messages
from .models import Juego
from myapp.src.login.forms import JuegoForm


def index(request):
    return render(request, 'index.html')

def register_account(request):
    return render(request, 'register_account.html')

def register_account_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Solo se llama una vez a form.save()
            user = form.save(commit=False)  # Evita guardarlo inmediatamente
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            # Guarda el usuario antes de autenticar
            user.save()
            
            # Iniciar sesión automáticamente
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Sesión iniciada")
                return redirect('/')  # Redirigir a la página de inicio
            else:
                messages.error(request, "No se pudo autenticar al usuario.")
        else:
            messages.error(request, "No se pudo registrar el usuario. Revisa los datos ingresados.")
    else:
        form = RegistroForm()  # Si es un GET, simplemente se carga el formulario vacío

    return render(request, 'register_account.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Sesión iniciada")
            return redirect('/')
        else:
            messages.error(request, "Credenciales inválidas. Inténtalo de nuevo.")
    return render(request, 'index.html')


def agregar_juego(request):
    if request.method == 'POST':
        form = JuegoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_juegos')  # Redirigir a la lista de juegos
    else:
        form = JuegoForm()

    return render(request, 'agregar_juego.html', {'form': form})


def lista_juegos(request):
    juegos = Juego.objects.all()
    return render(request, 'lista_juegos.html', {'juegos': juegos})

def index(request):
    juegos = Juego.objects.all()[:10]  # Obtiene todos los juegos
    return render(request, 'index.html', {'juegos': juegos})

def agregar_al_carrito(request, juego_id):
    # Obtener el producto o devolver un error 404 si no existe
    juego = get_object_or_404(Juego, id=juego_id)
    
    # Convertir el producto_id a cadena, ya que las claves en la sesión son strings
    juego_id_str = str(juego_id)
    
    # Obtener el carrito de la sesión, si no existe, inicializarlo como un diccionario vacío
    carrito = request.session.get('carrito', {})
    
    # Si el producto ya está en el carrito, incrementar la cantidad
    if juego_id_str in carrito:
        carrito[juego_id_str]['cantidad'] += 1
    else:
        # Agregar el producto al carrito con la cantidad inicial de 1
        carrito[juego_id_str] = {
            'nombre': juego.nombre,
            'precio': float(juego.precio),
            'cantidad': 1,
        }
    
    # Guardar el carrito en la sesión
    request.session['carrito'] = carrito
    
    return redirect('lista_juegos') #Cambiar por lista de juegos

@login_required
def ver_carrito(request):
    # Obtener el carrito de la sesión, si no existe, inicializarlo como un diccionario vacío
    carrito = request.session.get('carrito', {})
    
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())  # Calcular el total
    
    return render(request, 'carrito.html', {'carrito': carrito, 'total': total})

def eliminar_del_carrito(request, juego_id):
    # Convertir el producto_id a cadena
    juego_id_str = str(juego_id)
    
    # Obtener el carrito de la sesión
    carrito = request.session.get('carrito', {})
    
    # Si el producto está en el carrito, eliminarlo
    if juego_id_str in carrito:
        del carrito[juego_id_str]
    
    # Actualizar el carrito en la sesión
    request.session['carrito'] = carrito
    
    return redirect('carrito')

def vaciar_carrito(request):
    request.session['carrito'] = {}  # Vaciar el carrito en la sesión
    return redirect('carrito')
