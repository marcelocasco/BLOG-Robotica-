# apps/eventos/urls.py

from django.urls import path
from .views import (
    lista_eventos,
    detalle_evento,
    crear_evento,
    editar_evento,
    eliminar_evento
)

app_name = 'eventos'

urlpatterns = [
    # URL principal del app para listar todos los eventos
    path('', lista_eventos, name="lista_eventos"),

    # URL para ver los detalles de un evento específico
    path('<int:pk>/', detalle_evento, name="detalle_evento"),

    # URL para crear un nuevo evento
    path('crear/', crear_evento, name="crear_evento"),

    # URL para editar un evento existente
    path('editar/<int:pk>/', editar_evento, name="editar_evento"),

    # URL para eliminar un evento existente
    path('eliminar/<int:pk>/', eliminar_evento, name="eliminar_evento"),
]
