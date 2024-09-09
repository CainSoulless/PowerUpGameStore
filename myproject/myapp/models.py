from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.nombre
    

class Juego(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    imagen = models.ImageField(upload_to='myapp/static/assets/img', null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='juegos')

    def __str__(self):
        return f'{self.nombre} (ID: {self.id}) - Categoría: {self.categoria.nombre}'

    def get_id(self):
        return f"ID: {self.nombre}" 