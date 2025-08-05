from django.contrib import admin
from .models import Noticia, Categoria, Autor, Imagen, Video, Comentario, Persona

# -----------------------------------------------
# Usamos InlineModelAdmin para que las imágenes y videos se puedan
# agregar directamente desde la página de Noticia


class ImagenInline(admin.TabularInline):
    model = Imagen
    extra = 1  # Muestra un campo extra vacío por defecto


class VideoInline(admin.TabularInline):
    model = Video
    extra = 1

# --------------------------------------------


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    # inlines agregados a la lista
    inlines = [ImagenInline, VideoInline]

    fields = ('titulo', 'subtitulo', 'contenido', 'autor', 'categorias')

    list_display = ('titulo', 'fecha', 'autor')
    list_filter = ('fecha', 'autor', 'categorias')
    search_fields = ('titulo', 'autor__nombre')
    date_hierarchy = 'fecha'

# -----------------------------------------------------
# Registramos el resto de los modelos


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nacionalidad')
    search_fields = ('nombre',)


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('autor', 'noticia', 'fecha')


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
