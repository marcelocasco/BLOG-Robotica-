from django.db import models
from django.conf import settings
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class Categoria(models.Model):
    categoria_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class Autor(models.Model):
    autor_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    nacionalidad = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre


class Noticia(models.Model):
    noticia_id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=85)
    subtitulo = models.CharField(max_length=150, default='')
    contenido = models.TextField()
    fecha = models.DateField(auto_now_add=True)
    categorias = models.ManyToManyField(Categoria)  # Relacion n:m (muchos a muchos)
    # Relación 1:n (uno a muchos) con el usuario que publica la noticia
    autor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

    # Comentario: Ahora el campo autor referencia directamente al modelo User,
    # lo que permite comparar fácilmente con request.user y mostrar opciones solo al autor real.

# ----------------------------------------------------------------
# creado el 5/8 para poder subir imagenes y videos a la noticia

class Imagen(models.Model):
    imagen_id = models.AutoField(primary_key=True)
    noticia = models.ForeignKey(
        Noticia, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='noticias/imagenes/')
    descripcion = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return f"Imagen de '{self.noticia.titulo}'"


class Video(models.Model):
    video_id = models.AutoField(primary_key=True)
    noticia = models.ForeignKey(
        Noticia, on_delete=models.CASCADE, related_name='videos')
    url_video = models.URLField(max_length=500)
    descripcion = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return f"Video de '{self.noticia.titulo}'"

# -------------------------------------------------------------------


class Perfil(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    biografia = models.TextField()
    persona = models.OneToOneField(User, on_delete=models.CASCADE)
    # Campo para la foto de perfil del usuario
    foto_perfil = models.ImageField(upload_to='perfil/', blank=True, null=True)
    # Para mostrar la foto en el template, usar: perfil.foto_perfil.url


class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    noticia = models.ForeignKey(Noticia,on_delete=models.CASCADE)

    def __str__(self):
        return f"Comentario de {self.usuario.nombre} {self.usuario.apellido}"
