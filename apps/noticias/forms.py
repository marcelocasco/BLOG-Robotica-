from django import forms
from .models import Perfil
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
    # El campo foto_perfil se mostrará como input tipo file 
from django import forms
from .models import Noticia,Comentario
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class NoticiaForm(forms.ModelForm):
    imagen = forms.ImageField(required=False, label='Imagen de la noticia', widget=forms.ClearableFileInput(attrs={
        'class': 'w-full px-4 py-2 rounded-lg bg-neutral-800 border border-neutral-700 focus:ring-2 focus:ring-cyan-400 outline-none',
    }))
    # Campo para seleccionar una o varias categorías
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
