with open('equipamentos/models.py', 'w') as f:
    f.write('''from django.db import models
from django.core.validators import MinValueValidator

class Equipamento(models.Model):
    nome = models.CharField(max_length=255)
    marca = models.CharField(max_length=100)
    quantidade = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1, message='A quantidade deve ser maior que 0.')]
    )

    def __str__(self):
        return f"{self.nome} ({self.marca})"
''')

print('✓ models.py atualizado com validador de quantidade mínima')
