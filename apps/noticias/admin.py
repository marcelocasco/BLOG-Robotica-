from django.contrib import admin
from .models import Noticia, Categoria, Autor

class NoticiaAdmin(admin.ModelAdmin):
    fields = ('titulo', 'subtitulo', 'contenido', 'autor', 'categorias')

    list_display = ('titulo', 'fecha', 'autor')

    list_filter = ('fecha', 'autor', 'categorias')

    search_fields = ('titulo', 'autor')


admin.site.register(Noticia, NoticiaAdmin)
admin.site.register(Categoria)
admin.site.register(Autor)
