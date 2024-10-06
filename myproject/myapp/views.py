from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .src.login.forms import RegistroForm 
from django.contrib import messages
from django.http import JsonResponse
from .models import Juego
from .models import Categoria
from myapp.src.login.forms import JuegoForm
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse

# REST API
from rest_framework import generics
from .models import Juego, Categoria
from .serializers import JuegoSerializer, CategoriaSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .forms import UserProfileForm, UserEditForm
import requests

def index(request):
    return render(request, 'index.html')

def trivia(request):
    url = 'https://opentdb.com/api.php?amount=1&category=15&difficulty=easy&type=boolean'
    response = requests.get(url)
    
    preguntas = response.json().get('results', [])
    
    context = {
        'preguntas' : preguntas
    }
    
    return render(request, 'trivia.html', context)


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



def lista_juegos(request):
    juegos = Juego.objects.all()
    return render(request, 'lista_juegos.html', {'juegos': juegos})

def index(request):
    juegos = Juego.objects.all()[:10]  # Obtiene todos los juegos
    return render(request, 'index.html', {'juegos': juegos})

@login_required
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
    user_form = UserEditForm(instance=request.user)
    profile_form = UserProfileForm(instance=request.user.userprofile)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil_usuario')

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'perfil_usuario.html', context)

@user_passes_test(lambda u: u.is_superuser)
def gestionar_juegos(request):
    juegos = Juego.objects.all()  # Suponiendo que tienes un modelo llamado Juego
    return render(request, 'admin_panel/gestionar_juegos.html', {'juegos': juegos})

@user_passes_test(lambda u: u.is_superuser)
def editar_juego(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)
    
    if request.method == 'POST':
        form = JuegoForm(request.POST, instance=juego)
        if form.is_valid():
            form.save()
            return redirect('admin_panel/gestionar_juegos')  # Redirige de nuevo a la página de gestión
    else:
        form = JuegoForm(instance=juego)

    return render(request, 'admin_panel/editar_juego.html', {'form': form, 'juego': juego})

@user_passes_test(lambda u: u.is_superuser)
def eliminar_juego(request, juego_id):
    try:
        juego = get_object_or_404(Juego, id=juego_id)
        
        if request.method == 'POST':
            juego.delete()
            messages.success(request, f"El juego {juego.nombre} ha sido eliminado con éxito.")
            return redirect(reverse('gestionar_juegos'))
            
    except Juego.DoesNotExist:
        messages.error(request, "El juego no existe.")
        return redirect('gestionar_juegos')

    return render(request, 'admin_panel/eliminar_juego.html', {'juego': juego})


@user_passes_test(lambda u: u.is_superuser)
def agregar_juego(request):
    if request.method == 'POST':
        form = JuegoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'El juego ha sido agregado con éxito.')
            return redirect('gestionar_juegos')
        else:
            print(form.errors)  # Esto imprimirá los errores en la consola
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = JuegoForm()

    # Asegúrate de que las categorías estén disponibles en el contexto
    categorias = Categoria.objects.all()

    return render(request, 'admin_panel/agregar_juego.html', {'form': form, 'categorias': categorias})


def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'juegos/listar_categorias.html', {'categorias': categorias})

def listar_juegos(request):
    juegos = Juego.objects.all()
    paginator = Paginator(juegos, 10)  # Muestra 10 juegos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'juegos/listar_juegos.html', {'page_obj': page_obj})

class JuegoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Juego.objects.all()
    serializer_class = JuegoSerializer
    permission_classes = [IsAuthenticated]  # Requiere autenticación para acceder

class JuegoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Juego.objects.all()
    serializer_class = JuegoSerializer
    permission_classes = [IsAuthenticated]  # Requiere autenticación para acceder

# Vistas protegidas de Categoría
class CategoriaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]  # Requiere autenticación para acceder

class CategoriaDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]  # Requiere autenticación para acceder


class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_message = "El correo de restablecimiento ha sido enviado. Revisa tu bandeja de entrada."
    success_url = reverse_lazy('index')