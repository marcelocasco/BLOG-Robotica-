from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Evento, Categoria
from .forms import EventoForm



### Listar todos los eventos
# FBV
def eventos(request):
    eventos = Evento.objects.all()
    categorias = Categoria.objects.all()

    params = request.GET.get("categoria", "").strip()

    if params:
        eventos = eventos.filter(categorias__nombre__icontains=params)

    context = {"eventos": eventos, "categorias": categorias}
    return render(request, "eventos/eventos.html", context)


# CBV
class EventosView(ListView):
    model = Evento
    template_name = "eventos/eventos.html"
    context_object_name = "eventos"

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.GET.get("categoria", "").strip()
        if params:
            queryset = queryset.filter(categorias__nombre__icontains=params)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorias"] = Categoria.objects.all()
        return context


### Detalle de un evento
# FBV
def detalle_evento(request, evento_id):
    evento = Evento.objects.get(evento_id=evento_id)
    context = {"detalle": evento}
    return render(request, "eventos/detalle_evento.html", context)


# CBV
class DetalleEventoView(DetailView):
    model = Evento
    template_name = "eventos/detalle_evento.html"
    context_object_name = "detalle"
    pk_url_kwarg = "evento_id"





### Creación de un evento
# FBV
def crear_evento(request):
    if request.method == "POST":
        # Obtener la informacion del formulario que me envio el usuario de la página
        form = EventoForm(request.POST, request.FILES)

        if form.is_valid():
            # Guardar esa informacion en mi base de datos
            form.save()
            return redirect("todos_los_eventos")
    else:
        # mostrar el formulario vacío.
        form = EventoForm()

    context = {
        "form": form 
        }
    return render(request, "eventos/crear_evento.html", context)

# CBV
class CrearEventoView(CreateView):
    model = Evento
    template_name = "eventos/crear_evento.html"
    form_class = EventoForm
    success_url = reverse_lazy('todos_los_eventos')




### Editar un evento
# FBV
def editar_evento(request, evento_id):
    evento = Evento.objects.get(evento_id=evento_id)

    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            return redirect("detalle_evento", evento_id=evento.evento_id)
    else:
        form = EventoForm(instance=evento)

    return render(request, 'eventos/editar_evento.html', {"form": form})

# CBV
class EditarEventoView(UpdateView):
    model = Evento
    template_name = "eventos/editar_evento.html"
    form_class = EventoForm
    success_url = reverse_lazy('todos_los_eventos')
    pk_url_kwarg = 'evento_id'




### Eliminar un evento
# FBV
def eliminar_evento(request, evento_id):
    evento = Evento.objects.get(evento_id=evento_id)

    if request.method == 'POST':
        evento.delete()
        return redirect("todos_los_eventos")

    return render(request, 'eventos/eliminar_evento.html', {"evento": evento})

# CBV
class EliminarEventoView(DeleteView):
    model = Evento
    template_name = "eventos/eliminar_evento.html"
    success_url = reverse_lazy("todos_los_eventos")
    pk_url_kwarg = 'evento_id'

