from django.shortcuts import render, redirect,get_object_or_404
from .forms import NoticiaForm, RegistroUsuarioForm
from .models import Noticia
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, Http404

def inicio(request):
    return render(request, 'inicio.html')

@login_required
def noticia_nueva(request):
    if request.method == "POST":
        form = NoticiaForm(request.POST)
        if form.is_valid():
            noticia = form.save(commit=False)
            noticia.autor = request.user  # asignamos el usuario actual
            noticia.save()
            return redirect('lista_noticias')
    else:
        form = NoticiaForm()
    return render(request, 'noticia_form.html', {'form': form})


@login_required
def noticia_editar(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    if noticia.autor != request.user:
        return HttpResponseForbidden("No tenés permiso para editar esta noticia")
    
    if request.method == "POST":
        form = NoticiaForm(request.POST, instance=noticia)
        if form.is_valid():
            form.save()
            return redirect('lista_noticias')
    else:
        form = NoticiaForm(instance=noticia)
    return render(request, 'noticia_form.html', {'form': form})

def lista_noticias(request):
    noticias = Noticia.objects.order_by('-fecha')  # cambiamos a 'fecha'
    return render(request, 'lista_noticias.html', {'noticias': noticias})

def noticia_detalle(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    return render(request, 'noticia_detalle.html', {'noticia': noticia})


@login_required
def eliminar_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)

    if request.method == 'POST':
        noticia.delete()
        return redirect('lista_noticias')

    return render(request, 'noticia_confirmar_eliminar.html', {'noticia': noticia})


def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)  # inicia sesión automáticamente
            return redirect('inicio')  # nombre de tu vista principal
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form})

def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')  # Cambia 'inicio' por el nombre de tu vista principal


