from django.db import models

class Equipamento(models.Model):
    nome = models.CharField(max_length=255)
    marca = models.CharField(max_length=100)
    quantidade = models.PositiveIntegerField(default=0) # Garante que a quantidade não seja negativa

    def __str__(self):
        return f"{self.nome} ({self.marca})"
