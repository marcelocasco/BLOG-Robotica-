# eventos/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Evento  # Asume un modelo Evento
from .forms import EventoForm  # Asume un formulario EventoForm


def lista_eventos(request):
    eventos = Evento.objects.all().order_by('-fecha')
    return render(request, 'eventos/lista_eventos.html', {'eventos': eventos})


def detalle_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    return render(request, 'eventos/detalle_evento.html', {'evento': evento})


@login_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.autor = request.user
            evento.save()
            return redirect('eventos:detalle_evento', pk=evento.pk)
    else:
        form = EventoForm()
    return render(request, 'eventos/crear_evento.html', {'form': form})


@login_required
def actualizar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

    if request.user != evento.autor and not request.user.is_superuser:
        return redirect('eventos:detalle_evento', pk=evento.pk)

    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('eventos:detalle_evento', pk=evento.pk)
    else:
        form = EventoForm(instance=evento)

    return render(request, 'eventos/actualizar_evento.html', {'form': form, 'evento': evento})


@login_required
def eliminar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

    if request.user != evento.autor and not request.user.is_superuser:
        return redirect('eventos:detalle_evento', pk=evento.pk)

    if request.method == 'POST':
        evento.delete()
        return redirect('eventos:lista_eventos')

    return render(request, 'eventos/eliminar_evento.html', {'evento': evento})