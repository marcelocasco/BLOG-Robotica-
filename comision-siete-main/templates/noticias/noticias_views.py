# noticias/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Noticia, Categoria  # Asegúrate de que este modelo exista
from .forms import NoticiaForm  # Asumimos que tienes un formulario llamado NoticiaForm


def lista_noticias(request):
    """
    Vista para mostrar la lista de todas las noticias.
    """
    noticias = Noticia.objects.all().order_by('-fecha_publicacion')
    return render(request, 'noticias/todas_noticias.html', {'noticias': noticias})


def detalle_noticia(request, pk):
    """
    Vista para ver los detalles de una noticia específica.
    """
    noticia = get_object_or_404(Noticia, pk=pk)
    return render(request, 'noticias/una_noticia.html', {'noticia': noticia})


@login_required
def crear_noticia(request):
    """
    Vista para crear una nueva noticia.
    """
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            noticia = form.save(commit=False)
            noticia.autor = request.user
            noticia.save()
            return redirect('noticias:detalle_noticia', pk=noticia.pk)
    else:
        form = NoticiaForm()
    return render(request, 'noticias/crear_noticia.html', {'form': form})


@login_required
def actualizar_noticia(request, pk):
    """
    Vista para actualizar una noticia existente.
    Requiere que el usuario esté autenticado y sea el autor de la noticia.
    """
    noticia = get_object_or_404(Noticia, pk=pk)

    # Verifica si el usuario actual es el autor de la noticia o un superusuario
    if request.user != noticia.autor and not request.user.is_superuser:
        return redirect('noticias:detalle_noticia', pk=noticia.pk)

    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            form.save()
            return redirect('noticias:detalle_noticia', pk=noticia.pk)
    else:
        form = NoticiaForm(instance=noticia)

    return render(request, 'noticias/actualizar_noticia.html', {'form': form, 'noticia': noticia})


@login_required
def eliminar_noticia(request, pk):
    """
    Vista para eliminar una noticia.
    Requiere que el usuario esté autenticado y sea el autor.
    Muestra una página de confirmación (GET) o elimina la noticia (POST).
    """
    noticia = get_object_or_404(Noticia, pk=pk)

    # Verifica si el usuario actual es el autor de la noticia o un superusuario
    if request.user != noticia.autor and not request.user.is_superuser:
        return redirect('noticias:detalle_noticia', pk=noticia.pk)

    if request.method == 'POST':
        noticia.delete()
        # Redirigir a la lista de noticias después de la eliminación
        return redirect('noticias:lista_noticias')

    return render(request, 'noticias/eliminar_noticia.html', {'noticia': noticia})


def noticias_politica(request):
    """
    Vista para mostrar noticias de la categoría 'Política'.
    """
    noticias = Noticia.objects.filter(categoria__nombre='Política').order_by('-fecha_publicacion')
    return render(request, 'noticias/noticias_politica.html', {'noticias': noticias})