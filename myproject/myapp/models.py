from django.db import models
from django.contrib.auth.models import User
import os

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class Juego(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    imagen = models.ImageField(upload_to='uploads/', max_length=255, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='juegos')
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.imagen:
            # Limitar el nombre de la imagen a 100 caracteres
            self.imagen.name = os.path.basename(self.imagen.name)[:100]
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombre} - Categoría: {self.categoria.nombre}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)  # Campo para la imagen de perfil

    def __str__(self):
        return self.user.username

class Tarjeta(models.Model):
    nombre = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.nombre
    
class MetodosPago(models.Model):
    nombre = models.CharField(max_length=200)
    tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f'{self.nombre} - Tarjeta: {self.tarjeta.nombre}'
    
class Compra(models.Model):
    cliente = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pago = models.ForeignKey(MetodosPago, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.nombre} - Cliente: {self.cliente.user} - Forma de pago: {self.forma_pago.nombre}'

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
