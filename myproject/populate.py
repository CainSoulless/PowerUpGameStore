import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

django.setup()

from myapp.models import Categoria, Juego, Tarjeta, MetodosPago, Compra

Horror = Categoria.objects.create(
    nombre = "Horror",
    descripcion = "Contiene material que busca perturbar al jugador."
)

Shooter = Categoria.objects.create(
    nombre = "Shooter",
    descripcion = "Gameplay se basa en disparar armas en primera o tercera persona como forma de combate."
)

Aventura = Categoria.objects.create(
    nombre = "Aventura",
    descripcion = "Caracterizados por la investigación, exploración y solución de rompecabezas."
)

Pelea = Categoria.objects.create(
    nombre = "Pelea",
    descripcion = "Los juegos de pelea ponen a prueba tus reflejos y tu toma de decisiones contra tus oponentes."
)

Juego.objects.create(
    nombre = "Dead by Daylight",
    descripcion = "Juego de horror multijugador donde 4 jugadores deben cooperar para escapar de un jugador asesino en contra.",
    imagen = "myapp/static/assets/img/dbd.jpg",
    categoria = Horror,
    precio = 25000
)

Juego.objects.create(
    nombre = "Call of Duty Modern Warfare 3",
    descripcion = "Shooter en primera persona con un modo campaña y multijugador.",
    imagen = "myapp/static/assets/img/cod-mw3.jpg",
    categoria = Shooter,
    precio = 45000
)

Juego.objects.create(
    nombre = "Tekken 8",
    descripcion = "Entrada más reciente en la saga Tekken, tras la muerte de Heihachi ha llegado la hora del climax entre la rivalidad de Kazuya Mishima y Jin Kazama.",
    imagen = "myapp/static/assets/img/tekken-8.jpg",
    categoria = Pelea,
    precio = 45000
)

Juego.objects.create(
    nombre = "The legend of Zelda: Breath of the Wild",
    descripcion = "Sigue la aventura de Link mientras explora el mundo abierto de Hyrule en busca de una forma de derrotar la corrupción de Ganon.",
    imagen = "myapp/static/assets/img/aventura.jpg",
    categoria = Aventura,
    precio = 40000
)

Visa = Tarjeta.objects.create(
    nombre = "Visa",
)

Mastercard = Tarjeta.objects.create(
    nombre = "MasterCard",
)

No_tiene = Tarjeta.objects.create(
    nombre = "No es crédito",
)

MetodosPago.objects.create(
    nombre = "Tarjeta de Crédito Visa",
    tarjeta = Visa
)

MetodosPago.objects.create(
    nombre = "Tarjeta de Crédito Mastercard",
    tarjeta = Mastercard
)

MetodosPago.objects.create(
    nombre = "Tarjeta de Débito",
    tarjeta = No_tiene
)

MetodosPago.objects.create(
    nombre = "Paypal",
    tarjeta = No_tiene
)
