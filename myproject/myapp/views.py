from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .src.login.forms import RegistroForm 
from django.contrib import messages


# Create your views here.

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
            return redirect('home')  # Redirigir a la página de inicio
    else:
        form = RegistroForm()
    return render(request, 'register_account.html', {'form': form})
