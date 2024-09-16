from django.contrib import admin
from .models import Categoria
from .models import Juego
from .models import Tarjeta
from .models import MetodosPago
from .models import Compra

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Juego)
admin.site.register(Tarjeta)
admin.site.register(MetodosPago)
admin.site.register(Compra)
