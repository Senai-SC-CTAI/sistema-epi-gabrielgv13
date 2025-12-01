from django.db import models

class Colaborador(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True, help_text="Email único do colaborador")
    funcao = models.CharField(max_length=255, blank=True, null=True)
    # Adicione outros campos se precisar (ex: matrícula, cargo, etc.)

    def __str__(self):
        return self.nome
