from django.contrib import admin
from .models import Categoria, Autor, Noticia, Imagen, Video, Perfil, Comentario

# Registrar todos los modelos para que aparezcan en el admin
admin.site.register(Categoria)
admin.site.register(Autor)
admin.site.register(Noticia)
admin.site.register(Imagen)
admin.site.register(Video)
admin.site.register(Perfil)
admin.site.register(Comentario)
