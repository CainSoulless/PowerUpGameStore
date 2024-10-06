from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Juego, Categoria
from django.utils.crypto import get_random_string
import os

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['birthday', 'address', 'profile_image']  # Incluye el campo de la imagen

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'readonly': 'readonly'})  # El email no se puede cambiar
        }

class JuegoForm(forms.ModelForm):
    class Meta:
        model = Juego
        fields = ['nombre', 'descripcion', 'imagen', 'categoria', 'precio']

    def save(self, *args, **kwargs):
        juego = super().save(commit=False)
        if juego.imagen:
            extension = os.path.splitext(juego.imagen.name)[1]
            # Genera un nombre de archivo aleatorio
            juego.imagen.name = f"{get_random_string(10)}{extension}"
        juego.save()
        return juego
