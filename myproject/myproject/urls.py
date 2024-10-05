"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from myapp.views import register_account_view, login_view, ver_carrito, CustomPasswordResetView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from myapp.views import (
    JuegoListCreateAPIView, 
    JuegoDetailAPIView, 
    CategoriaListCreateAPIView, 
    CategoriaDetailAPIView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # Rutas del sitio web
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register_account/', register_account_view, name='register_account'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('juegos/', views.lista_juegos, name='lista_juegos'),
    path('juegos/listar_juegos', views.listar_juegos, name='listar_juegos'),
    path('juegos/listar_categorias', views.listar_categorias, name='listar_categorias'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:juego_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:juego_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('juego/<int:juego_id>/', views.detalle_juego, name='detalle_juego'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('admin_panel/gestionar-juegos/', views.gestionar_juegos, name='gestionar_juegos'),
    path('admin_panel/gestionar-juegos/editar/<int:juego_id>/', views.editar_juego, name='editar_juego'),
    path('admin_panel/gestionar-juegos/eliminar/<int:juego_id>/', views.eliminar_juego, name='eliminar_juego'),
    path('admin_panel/gestionar-juegos/agregar/', views.agregar_juego, name='agregar_juego'),

    # Rutas API con prefijo `api/`
    path('api/juegos/', JuegoListCreateAPIView.as_view(), name='api-juego-list'),
    path('api/juegos/<int:pk>/', JuegoDetailAPIView.as_view(), name='api-juego-detail'),
    path('api/categorias/', CategoriaListCreateAPIView.as_view(), name='api-categoria-list'),
    path('api/categorias/<int:pk>/', CategoriaDetailAPIView.as_view(), name='api-categoria-detail'),

    # 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Confirmación de que se ha enviado un correo
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    
    # Ruta para establecer una nueva contraseña usando el token enviado por correo
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # Confirmación de que la contraseña se ha restablecido con éxito
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
