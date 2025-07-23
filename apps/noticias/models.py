from django.db import models

class Categoria(models.Model):
    categoria_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Autor(models.Model):
    autor_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    nacionalidad = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Noticia(models.Model):
    noticia_id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=85)
    subtitulo = models.CharField(max_length=150)
    contenido = models.TextField()
    fecha = models.DateField(auto_now_add=True)
    categorias = models.ManyToManyField(Categoria) #Relacion n:m (muchos a muchos)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE) #Relación 1:n (uno a muchos)

    def __str__(self):
        return self.titulo  

# class Persona(models.Model):
#     id_persona = models.AutoField(primary_key=True)
#     nombre = models.CharField(max_length=100)
#     apellido = models.CharField(max_length=100)

# class Perfil(models.Model):
#     id_perfil = models.AutoField(primary_key=True)
#     biografia = models.TextField()
#     persona = models.OneToOneField(Persona, on_delete=models.CASCADE)

