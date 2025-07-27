# noticias/management/commands/seed_data.py

from django.core.management.base import BaseCommand
from noticias.models import Categoria, Autor, Noticia
from django.utils import timezone
import datetime  # Para asegurar que timezone.now() se use correctamente si es necesario, en models.py
# esta la automatizacion de fecha no hace falta, pero sirve para la base de datos hacerlo manual


class Command(BaseCommand):
    help = 'Seeds the database with initial categories, authors, and a sample news item.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(
            '--- Iniciando la siembra de datos ---'))

        # 1. Crear/Verificar Autor
        autor, created_autor = Autor.objects.get_or_create(
            nombre='Dr. Robótico',
            defaults={'nacionalidad': 'Internacional'}
        )
        if created_autor:
            self.stdout.write(self.style.SUCCESS(
                f"Autor '{autor.nombre}' creado."))
        else:
            self.stdout.write(self.style.WARNING(
                f"Autor '{autor.nombre}' ya existe."))

        # 2. Crear/Verificar Categorías de Robótica y otras
        categorias_a_crear = [
            ('Robots Industriales', 'Automatización y manufactura en entornos fabriles.'),
            ('Robots Móviles', 'Diseño y aplicación de vehículos autónomos y drones.'),
            ('Inteligencia Artificial en Robótica',
             'Implementación de aprendizaje automático y visión por computadora en robots.'),
            ('Sensores y Actuadores',
             'Componentes esenciales para la percepción del entorno y el movimiento robótico.'),
            ('Programación de Robots',
             'Desarrollo de algoritmos y software para el control y operación de robots.'),
            ('Aplicaciones de la Robótica',
             'Estudio de los diversos usos de la robótica en campos como la medicina, exploración, etc.'),
            ('Deportes', 'Noticias relacionadas con eventos deportivos.'),
            ('Tecnología', 'Innovaciones y avances tecnológicos.'),
            ('Política', 'Eventos y análisis políticos.'),
        ]

        self.stdout.write(self.style.HTTP_INFO(
            "\nVerificando/Creando categorías:"))
        for nombre, descripcion in categorias_a_crear:
            categoria_obj, created_cat = Categoria.objects.get_or_create(
                nombre=nombre,
                defaults={'descripcion': descripcion}
            )
            if created_cat:
                self.stdout.write(self.style.SUCCESS(
                    f"- Creada: '{categoria_obj.nombre}'"))
            else:
                self.stdout.write(self.style.WARNING(
                    f"- Ya existe: '{categoria_obj.nombre}'"))

        # 3. Crear/Verificar una Noticia de Ejemplo y Asignar Categorías
        noticia_titulo = 'Avances en Robots Colaborativos'
        noticia_subtitulo = 'La nueva generación de robots que trabajan junto a humanos en espacios compartidos.'
        noticia_contenido = 'Los cobots están revolucionando la manufactura, mejorando la seguridad y eficiencia.'

        noticia, created_noticia = Noticia.objects.get_or_create(
            titulo=noticia_titulo,
            defaults={
                'subtitulo': noticia_subtitulo,
                'contenido': noticia_contenido,
                'autor': autor,
                # 'fecha': timezone.now().date() # Solo si no tienes auto_now_add=True en el modelo, pero en models.py si esta
                # la automatizacion de fechas ,asi que dejo coomentado por si manualmente se quiere cambiar en base de datos.
            }
        )

        if created_noticia:
            self.stdout.write(self.style.SUCCESS(
                f"\nNoticia '{noticia.titulo}' creada."))
        else:
            self.stdout.write(self.style.WARNING(
                f"\nNoticia '{noticia.titulo}' ya existe."))

        # Asignar categorías a la noticia (solo si se creó o para asegurar)
        try:
            cat_industrial = Categoria.objects.get(
                nombre='Robots Industriales')
            cat_ia = Categoria.objects.get(
                nombre='Inteligencia Artificial en Robótica')
            cat_programacion = Categoria.objects.get(
                nombre='Programación de Robots')

            noticia.categorias.add(cat_industrial, cat_ia, cat_programacion)
            self.stdout.write(self.style.SUCCESS(
                f"Categorías asignadas a '{noticia.titulo}':"))
            for categoria in noticia.categorias.all():
                self.stdout.write(self.style.SUCCESS(f"- {categoria.nombre}"))
        except Categoria.DoesNotExist as e:
            self.stdout.write(self.style.ERROR(
                f"Error al asignar categorías: {e}. Asegúrate de que las categorías existen antes de intentar asignarlas."))

        self.stdout.write(self.style.SUCCESS(
            '\n--- Siembra de datos completa ---'))
