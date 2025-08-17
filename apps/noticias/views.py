# Vista para la página Sobre Nosotros

from .models import Perfil
from django.contrib.auth.decorators import login_required

from .forms import NoticiaForm, ImagenForm, VideoForm
from .models import Noticia, Comentario, Imagen, Video


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
    perfil, created = Perfil.objects.get_or_create(
        persona=request.user, defaults={'biografia': ''})
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
    noticias = Noticia.objects.order_by(
        '-fecha')[:10]  # Por ejemplo, las 10 últimas noticias
    return render(request, 'noticias/todas_noticias.html', {'noticias': noticias})


# ------------------------------------------------------


@login_required
def noticia_nueva(request):
    """
    Permite a un usuario autenticado crear una nueva noticia,
    incluyendo la subida de imágenes y videos.
    """
    if request.method == "POST":
        # Instanciar los formularios con los datos del POST y los archivos subidos
        form_noticia = NoticiaForm(request.POST)
        form_imagen = ImagenForm(request.POST, request.FILES)
        form_video = VideoForm(request.POST, request.FILES)

        # Validar todos los formularios que usas
        if form_noticia.is_valid() and form_imagen.is_valid() and form_video.is_valid():
            # 1. Guardar la noticia
            noticia = form_noticia.save(commit=False)
            noticia.autor = request.user
            noticia.save()

            # Guardar las categorías después de guardar la noticia
            categorias = form_noticia.cleaned_data.get('categorias')
            if categorias:
                noticia.categorias.set(categorias)

            # 2. Guardar la imagen si se proporcionó
            if form_imagen.cleaned_data.get('imagen'):
                imagen = form_imagen.save(commit=False)
                imagen.noticia = noticia
                imagen.save()

            # 3. Guardar el video si se proporcionó una URL o un archivo
            # La validación del formulario de video ya asegura que solo haya uno de los dos campos llenos
            url_video = form_video.cleaned_data.get('url_video')
            archivo_video = form_video.cleaned_data.get('archivo_video')

            if url_video or archivo_video:
                video = form_video.save(commit=False)
                video.noticia = noticia
                video.save()

            # Redireccionar a la página de inicio, por ejemplo
            return redirect('inicio')
    else:
        # Si no es un POST, inicializar los formularios vacíos
        form_noticia = NoticiaForm()
        form_imagen = ImagenForm()
        form_video = VideoForm()

    return render(request, 'noticias/noticia_form.html', {
        'form_noticia': form_noticia,
        'form_imagen': form_imagen,
        'form_video': form_video
    })


# -------------------------------------------------


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
        noticias = Noticia.objects.filter(
            categorias__nombre__iexact=categoria_nombre).order_by('-fecha')
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
