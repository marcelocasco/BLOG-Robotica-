from django.contrib import admin
from .models import Noticia, Categoria, Autor, Imagen, Video

#-----------------------------------------------
#creado 5/8

# Usamos InlineModelAdmin para que las imágenes y videos se puedan
# agregar directamente desde la página de Noticia
class ImagenInline(admin.TabularInline):
    model = Imagen
    extra = 1  # Muestra un campo extra vacío por defecto

class VideoInline(admin.TabularInline):
    model = Video
    extra = 1

#--------------------------------------------

@admin.register(Noticia) #inlines agregado 5/8
class NoticiaAdmin(admin.ModelAdmin):
    
    #  inlines agregados 5/8 a la lista
    inlines = [ImagenInline, VideoInline]
    
    fields = ('titulo', 'subtitulo', 'contenido', 'autor', 'categorias')

    list_display = ('titulo', 'fecha', 'autor')

    list_filter = ('fecha', 'autor', 'categorias')
#cambie de autor a autor__nombre para poder buscar por autor
    search_fields = ('titulo', 'autor__nombre')
    date_hierarchy = 'fecha' # busqueda por fecha, agregado 5/8
#-----------------------------------------------------
# Registramos el resto de los modelos, reemplazando sintaxis creado 5/8
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nacionalidad')
    search_fields = ('nombre',)

#-----------------------------------------------------------


#reemplace esto con los inline
'''
admin.site.register(Noticia, NoticiaAdmin)
admin.site.register(Categoria)
admin.site.register(Autor)
'''