from django.shortcuts import render, redirect
from .models import Noticia, Autor, Categoria

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


# VISTA BASADA EN CLASES (CBV)
class TodasLasNoticiasView(ListView):
    model = Noticia
    template_name = "noticias/todas_noticias.html"
    context_object_name = "noticias"

# VISTA BASADA EN FUNCIONES (FBV)
def todas_las_noticias(request):
    categoria_param = request.GET.get("categoria", "").strip()

    # Buscar todas las noticias desde la base de datos.
    noticias = Noticia.objects.all()

    if categoria_param:
        noticias = noticias.filter(categorias__nombre__icontains=categoria_param)

    # Meterlas en un contexto.
    context = {"noticias": noticias, "categoria_seleccionada": categoria_param}

    # Renderizar el html con el contexto.
    return render(request, "noticias/todas_noticias.html", context)





# VISTA BASADA EN CLASES (CBV)
class UnaNoticiaView(DetailView):
    model = Noticia
    template_name = "noticias/una_noticia.html"
    context_object_name = "noticia"
    pk_url_kwarg = "noticia_id"





# VISTA BASADA EN CLASES (CBV)
def una_noticia(request, noticia_id):
    noticia = Noticia.objects.get(noticia_id=noticia_id)
    context = {"noticia": noticia}
    return render(request, "noticias/una_noticia.html", context)





# VISTA BASADA EN CLASES (CBV)
class CrearNoticiaView(CreateView):
    model = Noticia
    template_name = "noticias/nueva_noticia.html"
    fields = ["titulo", "subtitulo", "contenido"]
    success_url = reverse_lazy("todas_las_noticias")

# VISTA BASADA EN FUNCIONES (FBV)
class ActualizarNoticiaView(UpdateView):
    model = Noticia
    template_name = "noticias/actualizar_noticia.html"
    fields = ["titulo", "subtitulo"]
    success_url = reverse_lazy("todas_las_noticias")
    pk_url_kwarg = "noticia_id"





# VISTA BASADA EN CLASES (CBV)
class EliminarNoticiaView(DeleteView):
    model = Noticia
    template_name = "noticias/eliminar_noticia.html"
    success_url = reverse_lazy("todas_las_noticias")
    pk_url_kwarg = "noticia_id"

# VISTA BASADA EN FUNCIONES (FBV)
def eliminar_noticia(request, noticia_id):
    noticia = Noticia.objects.get(noticia_id=noticia_id)

    if request.method == "POST":
        noticia.delete()
        return redirect("todas_las_noticias_fbv")

    return render(request, "noticias/eliminar_noticia.html", {"noticia": noticia})