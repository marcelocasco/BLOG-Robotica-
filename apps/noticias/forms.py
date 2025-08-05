# apps/noticias/forms.py
from django import forms
from .models import Noticia, Imagen, Video


class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['titulo', 'subtitulo', 'contenido', 'categorias', 'autor']
