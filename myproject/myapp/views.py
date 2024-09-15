from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .src.login.forms import RegistroForm 
from django.contrib import messages
from django.http import JsonResponse
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
    juego = get_object_or_404(Juego, id=juego_id)
    carrito = request.session.get('carrito', {})

    if str(juego_id) in carrito:
        carrito[str(juego_id)]['cantidad'] += 1
    else:
        carrito[str(juego_id)] = {
            'id': juego.id,  # Asegúrate de almacenar el ID correctamente
            'nombre': juego.nombre,
            'precio': float(juego.precio),
            'cantidad': 1,
        }

    request.session['carrito'] = carrito
    return redirect('ver_carrito')


@login_required
def ver_carrito(request):
    # Obtener el carrito de la sesión, si no existe, inicializarlo como un diccionario vacío
    carrito = request.session.get('carrito', {})
    
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())  # Calcular el total
    
    return render(request, 'carrito.html', {'carrito': carrito, 'total': total})

def eliminar_del_carrito(request, juego_id):
    carrito = request.session.get('carrito', {})

    # Verifica si el juego está en el carrito y elimínalo
    if str(juego_id) in carrito:
        del carrito[str(juego_id)]
        request.session['carrito'] = carrito

    return redirect('ver_carrito')

# def eliminar_del_carrito(request, juego_id):
#     # Convertir el producto_id a cadena
#     juego_id_str = str(juego_id)
    
#     # Obtener el carrito de la sesión
#     carrito = request.session.get('carrito', {})
    
#     # Si el producto está en el carrito, eliminarlo
#     if juego_id_str in carrito:
#         del carrito[juego_id_str]
    
#     # Actualizar el carrito en la sesión
#     request.session['carrito'] = carrito
    
#     return redirect('carrito')

def vaciar_carrito(request):
    request.session['carrito'] = {}  # Vaciar el carrito en la sesión
    return redirect('carrito')

def detalle_juego(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)
    
    # Verificar si hay un juego agregado al carrito en la sesión
    juego_agregado = request.session.get('juego_agregado', False)
    
    # Eliminar la variable de sesión después de usarla
    if 'juego_agregado' in request.session:
        del request.session['juego_agregado']
    
    return render(request, 'detalle_juego.html', {
        'juego': juego,
        'juego_agregado': juego_agregado
    })

@login_required
def perfil_usuario(request):
    return render(request, 'perfil_usuario.html', {'usuario': request.user})