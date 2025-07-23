from django.db import models
from datetime import timedelta


class Organizador(models.Model):
    class TipoOrganizador(models.TextChoices):
        INDIVIDUAL = 'individual'
        EMPRESA = 'empresa'
        INSTITUCION = 'institucion'
    
    organizador_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    tipo = models.CharField(
        max_length=11,
        choices=TipoOrganizador.choices,
        default=TipoOrganizador.INDIVIDUAL
    )

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    categoria_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class Evento(models.Model):
    evento_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    inicio = models.DateTimeField()
    duracion_en_minutos = models.PositiveIntegerField(help_text="Duración en minutos.")
    organizador = models.ForeignKey(Organizador, on_delete=models.CASCADE)
    categorias = models.ManyToManyField(Categoria)
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True)

    def __str__(self):
        return self.nombre
    
    def fin(self):
        return self.inicio + timedelta(minutes=self.duracion_en_minutos)