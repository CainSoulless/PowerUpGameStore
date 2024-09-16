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
from myapp.views import register_account_view
from myapp.views import login_view
from myapp.views import ver_carrito
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
    

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register_account/', register_account_view, name='register_account'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('juegos/', views.lista_juegos, name='lista_juegos'),
    path('carrito/', ver_carrito, name='carrito'),
    path('carrito/agregar/<int:juego_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:juego_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('juego/<int:juego_id>/', views.detalle_juego, name='detalle_juego'),
    path('carrito/agregar/<int:juego_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('admin_panel/gestionar-juegos/', views.gestionar_juegos, name='gestionar_juegos'),
    path('admin_panel/gestionar-juegos/editar/<int:juego_id>/', views.editar_juego, name='editar_juego'),
    path('admin_panel/gestionar-juegos/eliminar/<int:juego_id>/', views.eliminar_juego, name='eliminar_juego'),
    path('admin_panel/gestionar-juegos/agregar/', views.agregar_juego, name='agregar_juego'),
    path('juegos/listar_categorias/', views.listar_categorias, name='listar_categorias'),
    path('juegos/listar_juegos/', views.listar_juegos, name='listar_juegos'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
