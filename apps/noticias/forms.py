# En tu archivo forms.py

from django import forms
# Asegúrate de que todos los modelos están importados
from .models import Noticia, Comentario, Imagen, Video, Perfil
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Formulario para editar la biografía del perfil


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['biografia', 'foto_perfil']
        widgets = {
            'biografia': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-neutral-800 border border-neutral-700 focus:ring-2 focus:ring-cyan-400 outline-none',
                'rows': 4,
                'placeholder': 'Escribe tu biografía...'
            }),
        }


class NoticiaForm(forms.ModelForm):
    categorias = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'mr-2 accent-cyan-400',
        }),
        required=True,
        label='Categorías'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Categoria
        self.fields['categorias'].queryset = Categoria.objects.all()

    class Meta:
        model = Noticia
        fields = ['titulo', 'contenido', 'categorias']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-neutral-800 border border-neutral-700 focus:ring-2 focus:ring-cyan-400 outline-none',
                'placeholder': 'Título de la noticia'
            }),
            'contenido': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-neutral-800 border border-neutral-700 focus:ring-2 focus:ring-cyan-400 outline-none',
                'rows': 6,
                'placeholder': 'Contenido de la noticia'
            }),
        }


class ImagenForm(forms.ModelForm):
    class Meta:
        model = Imagen
        fields = ['imagen', 'descripcion']
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-neutral-800 border border-neutral-700 focus:ring-2 focus:ring-cyan-400 outline-none',
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-neutral-800 border border-neutral-700 focus:ring-2 focus:ring-cyan-400 outline-none',
                'placeholder': 'Descripción de la imagen (opcional)'
            }),
        }


class VideoForm(forms.ModelForm):

    class Meta:
        model = Video
        fields = ['url_video', 'archivo_video', 'descripcion']

        # el codigo comentado daria obligatoriedad si es que si o si debe subir un video
    '''
    def clean(self):
       cleaned_data = super().clean()
       url_video = cleaned_data.get('url_video')
        archivo_video = cleaned_data.get('archivo_video')

        if not url_video and not archivo_video:
            raise forms.ValidationError(
                "Debes proporcionar una URL o subir un archivo de video.")

        if url_video and archivo_video:
            raise forms.ValidationError(
                "No puedes proporcionar una URL y subir un archivo de video al mismo tiempo.")
'''
    class Meta:
        model = Video
        fields = ['url_video', 'archivo_video', 'descripcion']
        widgets = {
            'url_video': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-neutral-800 border border-neutral-700 focus:ring-2 focus:ring-cyan-400 outline-none',
                'placeholder': 'URL del video (YouTube, Vimeo, etc.)'
            }),
            'archivo_video': forms.ClearableFileInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-neutral-800 border border-neutral-700 focus:ring-2 focus:ring-cyan-400 outline-none',
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-neutral-800 border border-neutral-700 focus:ring-2 focus:ring-cyan-400 outline-none',
                'placeholder': 'Descripción del video (opcional)'
            }),
        }


class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribí tu comentario aquí...'}),
        }
