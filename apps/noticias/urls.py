from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# Esta línea agrega rutas para servir archivos de medios (imágenes, etc.) en modo desarrollo.
# Django va a usar estas rutas para mostrar los archivos subidos en MEDIA_ROOT cuando este DEBUG=True.
urlpatterns = [
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('nueva/', views.noticia_nueva, name='noticia_nueva'),
    path('noticias/', views.lista_noticias, name='todas_noticias'),
    path('registro/', views.registro, name='registro'),
    path('editar/<int:pk>/', views.noticia_editar, name='noticia_editar'),
    path('detalle/<int:pk>/', views.noticia_detalle, name='noticia_detalle'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('noticia/<int:pk>/eliminar/', views.eliminar_noticia, name='eliminar_noticia'),
    path('comentario/<int:comentario_id>/eliminar/', views.eliminar_comentario, name='eliminar_comentario'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('sobre-nosotros/', views.sobre_nosotros, name='sobre_nosotros'),  # Ruta para la página Sobre Nosotros
]
