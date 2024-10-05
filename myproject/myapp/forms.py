from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

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
