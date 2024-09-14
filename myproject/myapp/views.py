from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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
