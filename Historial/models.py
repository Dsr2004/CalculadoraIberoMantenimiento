from django.db import models
from django.contrib.auth.models import User

class Historial(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    operacion = models.CharField(max_length=255)
    resultado = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.operacion} = {self.resultado}"
