# comsiete/views.py
from django.shortcuts import render
from apps.noticias.models import Noticia  # Importa el modelo de noticias


def inicio(request):
    """
    Vista de la página de inicio.
    Muestra las últimas 5 noticias para hacer la página más dinámica.
    """
    ultimas_noticias = Noticia.objects.all().order_by('-fecha')[:5]

    context = {
        'ultimas_noticias': ultimas_noticias
    }
    return render(request, 'index.html', context)