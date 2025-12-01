from django.db import models
from colaboradores.models import Colaborador
from equipamentos.models import Equipamento

class Emprestimo(models.Model):
    STATUS_CHOICES = [
        ('EMPRESTADO', 'Emprestado'),
        ('DEVOLVIDO', 'Devolvido'),
    ]

    nome = models.ForeignKey(Colaborador, on_delete=models.PROTECT, verbose_name="Colaborador")
    equipamento = models.ForeignKey(Equipamento, on_delete=models.PROTECT, verbose_name="Equipamento")
    quantidade = models.PositiveIntegerField(default=1, help_text="Quantidade emprestada")
    data_emprestimo = models.DateTimeField(auto_now_add=True, verbose_name="Data do Empréstimo")
    data_prazo = models.DateTimeField(verbose_name="Data de Devolução Prevista")
    data_devolucao_real = models.DateTimeField(null=True, blank=True, verbose_name="Data de Devolução Real")
    estoque_disponivel = models.PositiveIntegerField(default=0, help_text="Quantidade disponível no estoque após empréstimo")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='EMPRESTADO', verbose_name="Status")
    
    def __str__(self):
        return f"{self.nome.nome} - {self.equipamento.nome} ({self.quantidade}) - {self.get_status_display()}"
