from django.urls import path
from . import views

urlpatterns = [

    path('', views.inicio, name='inicio'),
    path('nueva/', views.noticia_nueva, name='noticia_nueva'),
    path('noticias/', views.lista_noticias, name='lista_noticias'),
    path('registro/', views.registro, name='registro'),
    path('editar/<int:pk>/', views.noticia_editar, name='noticia_editar'),
    path('detalle/<int:pk>/', views.noticia_detalle, name='noticia_detalle'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('noticia/<int:pk>/eliminar/', views.eliminar_noticia, name='eliminar_noticia'),
]
