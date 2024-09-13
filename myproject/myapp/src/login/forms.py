from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from myapp.models import UserProfile

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=100, required=True)
    birthday = forms.DateField(required=True)
    address = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'birthday', 'address', 'password1', 'password2']

    def save(self, commit=True):
        user = super(RegistroForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['full_name']
        
        if commit:
            user.save()
    
            # Evitar la duplicación de perfiles
            if not UserProfile.objects.filter(user=user).exists():
                UserProfile.objects.create(user=user, birthday=self.cleaned_data['birthday'], address=self.cleaned_data['address'])
            else:
                raise forms.ValidationError("El perfil de usuario ya existe.")
        
        return user

    # def save(self, commit=True):
    #     user = super(RegistroForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     user.first_name = self.cleaned_data['full_name']
    #     if commit:
    #         user.save()
    #         # Crear el UserProfile relacionado
    #         UserProfile.objects.create(user=user, birthday=self.cleaned_data['birthday'], address=self.cleaned_data['address'])
    #     return user
