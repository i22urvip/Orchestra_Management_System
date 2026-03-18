from django.db import models
from django.contrib.auth.models import User

class Compositor(models.Model):
    nombre = models.CharField(max_length=150)
    biografia = models.TextField(blank=True, null=True)
    epoca = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Obra(models.Model):
    TIPOS_DE_OBRA = [
        ('requiem', 'Réquiem'),
        ('vals', 'Vals'),
        ('sinfonia', 'Sinfonía'),
        ('sonata', 'Sonata'),
        ('concierto', 'Concierto'),
        ('otro', 'Otro'),
    ]

    titulo = models.CharField(max_length=200)
    compositor = models.ForeignKey(Compositor, on_delete=models.CASCADE, related_name='obras')
    tipo = models.CharField(max_length=50, choices=TIPOS_DE_OBRA)
    ano_composicion = models.IntegerField(help_text="Año en el que se compuso")
    duracion_minutos = models.IntegerField(help_text="Duración estimada en minutos")
    num_instrumentos = models.IntegerField(help_text="Número de instrumentos necesarios")
    partitura = models.FileField(upload_to='partituras/', blank=True, null=True)
    popularidad = models.IntegerField(default=0, help_text="Número de consultas/descargas")
    creador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    audio = models.FileField(upload_to='audios/', null=True, blank=True)

    def __str__(self):
        return f"{self.titulo} - {self.compositor.nombre}"