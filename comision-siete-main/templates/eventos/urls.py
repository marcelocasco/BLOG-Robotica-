# eventos/urls.py
from django.urls import path
from . import views

app_name = 'eventos'

urlpatterns = [
    path('', views.lista_eventos, name="lista_eventos"),
    path('<int:pk>/', views.detalle_evento, name="detalle_evento"),
    path('crear/', views.crear_evento, name="crear_evento"),
    path('actualizar/<int:pk>/', views.actualizar_evento, name="actualizar_evento"),
    path('eliminar/<int:pk>/', views.eliminar_evento, name="eliminar_evento"),
]
