from django.urls import path
from .views import (
    eventos, 
    EventosView, 
    detalle_evento,
    DetalleEventoView,
    crear_evento,
    CrearEventoView,
    editar_evento,
    EditarEventoView,
    eliminar_evento,
    EliminarEventoView
)


# localhost:8000/eventos/
urlpatterns = [
    path('', eventos, name="todos_los_eventos"),
    # path('', EventosView.as_view(), name="todos_los_eventos"),

    path('<int:evento_id>/', detalle_evento, name="detalle_evento"),
    # path('<int:evento_id>/', DetalleEventoView.as_view(), name="detalle_evento"),

    path('crear/', crear_evento, name="crear_evento"),
    # path('crear/', CrearEventoView.as_view(), name="crear_evento"),
    
    path('editar/<int:evento_id>/', editar_evento, name="editar_evento"),
    # path('editar/<int:evento_id>/', EditarEventoView.as_view(), name="editar_evento"),

    path('eliminar/<int:evento_id>/', eliminar_evento, name="eliminar_evento")
    # path('eliminar/<int:evento_id>/', EliminarEventoView.as_view(), name="eliminar_evento")
    
]