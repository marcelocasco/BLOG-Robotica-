# noticias/urls.py
from django.urls import path
from . import views

# Define el nombre del espacio de nombres de la aplicación para evitar conflictos con otras apps
app_name = 'noticias'

urlpatterns = [
    # URL para la lista de todas las noticias (página principal de la app)
    # Ejemplo de URL: /noticias/
    path('', views.lista_noticias, name="lista_noticias"),

    # URL para ver los detalles de una noticia específica por su clave primaria (pk)
    # Ejemplo de URL: /noticias/123/
    path('<int:pk>/', views.detalle_noticia, name="detalle_noticia"),

    # URL para crear una nueva noticia
    # Ejemplo de URL: /noticias/crear/
    path('crear/', views.crear_noticia, name="crear_noticia"),

    # URL para actualizar una noticia existente por su pk
    # Ejemplo de URL: /noticias/actualizar/123/
    path('actualizar/<int:pk>/', views.actualizar_noticia, name="actualizar_noticia"),

    # URL para eliminar una noticia existente por su pk
    # Ejemplo de URL: /noticias/eliminar/123/
    path('eliminar/<int:pk>/', views.eliminar_noticia, name="eliminar_noticia"),

    # URL para mostrar noticias de una categoría específica (ej: 'Política')
    # Ejemplo de URL: /noticias/politica/
    path('politica/', views.noticias_politica, name="noticias_politica"),
]