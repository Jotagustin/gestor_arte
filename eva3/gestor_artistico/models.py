from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.

class Artista(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Proyecto(models.Model):
    titulo = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo
    
class Colaboracion(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    valor = models.IntegerField(default=0)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.proyecto.titulo} - {self.artista.nombre}"
    

class PerfilUsuario(models.Model):

    class Rol(models.TextChoices):
        ADMIN = 'Admin'
        ARTISTA = 'Artista'
        GESTOR = 'Gestor'

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    rol = models.CharField(
        max_length=20,
        choices=Rol.choices,
        default=Rol.ARTISTA
    )


class Historial(models.Model):

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    accion = models.CharField(max_length=50)  
    tabla_afectada = models.CharField(max_length=50)
    registro_afectado_id = models.IntegerField(null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.fecha_hora}] {self.usuario}: {self.accion} en {self.tabla_afectada}"

