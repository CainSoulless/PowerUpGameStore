from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Juego, Categoria

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
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=True, empty_label="Seleccione una categoría")

    class Meta:
        model = Juego
        fields = ['nombre', 'descripcion', 'precio', 'categoria', 'imagen']