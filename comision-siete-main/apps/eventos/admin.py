from django.contrib import admin
from .models import Evento, Categoria, Organizador

admin.site.register(Evento)
admin.site.register(Categoria)
admin.site.register(Organizador)
