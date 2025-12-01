from django.db import models

class Colaborador(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True, help_text="Email único do colaborador")
    funcao = models.CharField(max_length=255, blank=True, null=True)
    # Adicione outros campos se precisar (ex: matrícula, cargo, etc.)

    def __str__(self):
        return self.nome

class Equipamento(models.Model):
    nome = models.CharField(max_length=255)
    marca = models.CharField(max_length=100)
    quantidade = models.PositiveIntegerField(default=0) # Garante que a quantidade não seja negativa

    def __str__(self):
        return f"{self.nome} ({self.marca})"