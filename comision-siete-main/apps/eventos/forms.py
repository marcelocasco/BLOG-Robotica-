from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'inicio', 'duracion_en_minutos', 'organizador', 'categorias', 'imagen']
        widgets = {
            'inicio': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                },
                format='%Y-%m-%d%H:%M'
            )
        }
        
