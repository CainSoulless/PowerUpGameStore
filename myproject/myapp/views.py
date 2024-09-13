from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .src.login.forms import RegistroForm 
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def register_account(request):
    return render(request, 'register_account.html')

def register_account_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # Iniciar sesión automáticamente
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Sesión iniciada")
            return redirect('/')  # Redirigir a la página de inicio
    else:
        form = RegistroForm()
        messages.error(request, "No se pudo iniciar sesión")
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