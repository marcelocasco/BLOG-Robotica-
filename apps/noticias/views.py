# Vista para la página Sobre Nosotros

from .models import Perfil
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from .forms import NoticiaForm, RegistroUsuarioForm, ComentarioForm
from .models import Noticia, Comentario
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, Http404

def sobre_nosotros(request):
    """
    Muestra la página de información sobre el equipo y el blog.
    """
    return render(request, 'noticias/sobre_nosotros.html')


# Vista de perfil de usuario
@login_required
def perfil_usuario(request):
    from .forms import PerfilForm
    perfil, created = Perfil.objects.get_or_create(persona=request.user, defaults={'biografia': ''})
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil_usuario')
    else:
        form = PerfilForm(instance=perfil)
    return render(request, 'noticias/perfil.html', {'usuario': request.user, 'perfil': perfil, 'form': form})



@login_required  # Solo usuarios autenticados pueden ver la página de inicio y las noticias
def inicio(request):
    """
    Vista para la página de inicio.
    Muestra la lista de las últimas noticias.
    Si el usuario no está autenticado, va a ser redirigido al login automáticamente.
    """
    noticias = Noticia.objects.order_by('-fecha')[:10]  # Por ejemplo, las 10 últimas noticias
    return render(request, 'noticias/todas_noticias.html', {'noticias': noticias})


@login_required
def noticia_nueva(request):
    """
    Permite a un usuario autenticado crear una nueva noticia.
    """
    if request.method == "POST":
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            noticia = form.save(commit=False)
            # Ahora el campo autor es el usuario autenticado
            noticia.autor = request.user
            noticia.save()
            # Guardar las categorías seleccionadas
            categorias = form.cleaned_data.get('categorias')
            if categorias:
                noticia.categorias.set(categorias)
            # Si se subió una imagen, crear el objeto Imagen relacionado
            imagen_archivo = form.cleaned_data.get('imagen')
            if imagen_archivo:
                from .models import Imagen
                Imagen.objects.create(noticia=noticia, imagen=imagen_archivo)
            return redirect('todas_noticias')
    else:
        form = NoticiaForm()
    return render(request, 'noticias/noticia_form.html', {'form': form})


@login_required
def noticia_editar(request, pk):
    """
    Permite al autor de una noticia editarla.
    """
    noticia = get_object_or_404(Noticia, pk=pk)
    if noticia.autor != request.user:
        return HttpResponseForbidden("No tenés permiso para editar esta noticia")
    
    if request.method == "POST":
        form = NoticiaForm(request.POST, instance=noticia)
        if form.is_valid():
            form.save()
            return redirect('todas_noticias')
    else:
        form = NoticiaForm(instance=noticia)
    return render(request, 'noticia_form.html', {'form': form})


@login_required
def eliminar_noticia(request, pk):
    """
    Permite al autor de una noticia eliminarla.
    """
    noticia = get_object_or_404(Noticia, pk=pk)
    if noticia.autor != request.user:
        return HttpResponseForbidden("No tenés permiso para eliminar esta noticia")
    if request.method == 'POST':
        noticia.delete()
    return redirect('todas_noticias')
    

@login_required  # Solo usuarios autenticados pueden ver la lista de noticias
def lista_noticias(request):
    """
    Muestra una lista de todas las noticias.
    Si el usuario no está autenticado, será redirigido al login automáticamente.
    """
    categoria_nombre = request.GET.get('categoria')
    if categoria_nombre:
        # Filtrar noticias por nombre de categoría (case-insensitive)
        noticias = Noticia.objects.filter(categorias__nombre__iexact=categoria_nombre).order_by('-fecha')
    else:
        noticias = Noticia.objects.order_by('-fecha')
    return render(request, 'noticias/todas_noticias.html', {
        'noticias': noticias,
        'categoria_seleccionada': categoria_nombre
    })


def noticia_detalle(request, pk):
    """
    Muestra los detalles de una noticia y permite agregar comentarios.
    """
    noticia = get_object_or_404(Noticia, pk=pk)
    comentarios = noticia.comentario_set.order_by('-fecha')

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ComentarioForm(request.POST)
            if form.is_valid():
                nuevo_comentario = form.save(commit=False)
                nuevo_comentario.noticia = noticia
                # Asignar correctamente el usuario que comenta
                nuevo_comentario.usuario = request.user
                nuevo_comentario.save()
                return redirect('noticia_detalle', pk=pk)
        else:
            return redirect('login')
    else:
        form = ComentarioForm()

    return render(request, 'noticias/noticia_detalle.html', {
        'noticia': noticia,
        'comentarios': comentarios,
        'form': form,
    })


def registro(request):
    """
    Permite a un nuevo usuario registrarse.
    """
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('inicio')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'noticias/registro.html', {'form': form})


def cerrar_sesion(request):
    """
    Cierra la sesión del usuario.
    """
    logout(request)
    return redirect('login')


@login_required
def eliminar_comentario(request, comentario_id):
    """
    Permite al autor de un comentario eliminarlo.
    """
    comentario = get_object_or_404(Comentario, id=comentario_id)
    
    if comentario.usuario != request.user:
        return HttpResponseForbidden("No tienes permiso para eliminar este comentario.")

    if request.method == "POST":
        comentario.delete()
        return redirect('noticia_detalle', pk=comentario.noticia.pk)

    return redirect('noticia_detalle', pk=comentario.noticia.pk)