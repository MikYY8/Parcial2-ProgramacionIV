from django.db import models
from django.conf import settings

class Alumno(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Reporte(models.Model):
    nombre = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha = models.DateField()

    def __str__(self):
        return self.nombre
