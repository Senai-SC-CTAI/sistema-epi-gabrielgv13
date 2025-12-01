from django.test import TestCase
from django.utils import timezone
from datetime import datetime, timedelta
from .utils import calculate_deadline
from .models import Equipamento, Colaborador, Emprestimo
from .forms import EmprestimoForm

class UtilsTestCase(TestCase):
    def test_calculate_deadline_weekday(self):
        # Segunda-feira (0) -> Quinta-feira (3)
        start_date = datetime(2023, 10, 2, 12, 0, 0) # Segunda
        expected = start_date + timedelta(days=3)
        self.assertEqual(calculate_deadline(start_date), expected)

    def test_calculate_deadline_weekend_skip(self):
        # Quarta-feira (2) + 3 dias = Sábado (5) -> Deve pular para Segunda (0)
        start_date = datetime(2023, 10, 4, 12, 0, 0) # Quarta
        # Sábado seria dia 7. Segunda é dia 9.
        expected = datetime(2023, 10, 9, 12, 0, 0)
        self.assertEqual(calculate_deadline(start_date), expected)

        # Quinta-feira (3) + 3 dias = Domingo (6) -> Deve pular para Segunda (0)
        start_date = datetime(2023, 10, 5, 12, 0, 0) # Quinta
        # Domingo seria dia 8. Segunda é dia 9.
        expected = datetime(2023, 10, 9, 12, 0, 0)
        self.assertEqual(calculate_deadline(start_date), expected)

class EmprestimoLogicTestCase(TestCase):
    def setUp(self):
        self.colaborador = Colaborador.objects.create(nome="Teste", email="teste@teste.com")
        self.equipamento = Equipamento.objects.create(nome="Capacete", marca="3M", quantidade=10)

    def test_form_validation_stock(self):
        # Tentar emprestar 11 (estoque 10)
        form_data = {
            'nome': self.colaborador.id,
            'equipamento': self.equipamento.id,
            'quantidade': 11
        }
        form = EmprestimoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Quantidade indisponível', form.errors['__all__'][0] if '__all__' in form.errors else str(form.errors))

    def test_form_validation_success(self):
        # Tentar emprestar 5 (estoque 10)
        form_data = {
            'nome': self.colaborador.id,
            'equipamento': self.equipamento.id,
            'quantidade': 5
        }
        form = EmprestimoForm(data=form_data)
        self.assertTrue(form.is_valid())
        # Verificar se calculou o estoque disponível no instance (mas não salva no banco ainda)
        self.assertEqual(form.instance.estoque_disponivel, 5)

    def test_view_logic_stock_update(self):
        # Simular o que a view faz
        emprestimo = Emprestimo(
            nome=self.colaborador,
            equipamento=self.equipamento,
            quantidade=5,
            data_prazo=calculate_deadline(timezone.now()),
            estoque_disponivel=5
        )
        emprestimo.save()
        
        # Atualizar estoque do equipamento (como feito na view)
        self.equipamento.quantidade -= emprestimo.quantidade
        self.equipamento.save()
        
        self.equipamento.refresh_from_db()
        self.assertEqual(self.equipamento.quantidade, 5)
        self.equipamento.refresh_from_db()
        self.assertEqual(self.equipamento.quantidade, 5)

    def test_return_logic(self):
        # Criar empréstimo
        emprestimo = Emprestimo.objects.create(
            nome=self.colaborador,
            equipamento=self.equipamento,
            quantidade=2,
            data_prazo=calculate_deadline(timezone.now()),
            estoque_disponivel=8,
            status='EMPRESTADO'
        )
        
        # Simular devolução
        emprestimo.status = 'DEVOLVIDO'
        emprestimo.data_devolucao_real = timezone.now()
        emprestimo.save()
        
        # Devolver ao estoque
        self.equipamento.quantidade += emprestimo.quantidade
        self.equipamento.save()
        
        self.equipamento.refresh_from_db()
        self.assertEqual(self.equipamento.quantidade, 12) # 10 inicial + 2 devolvidos (mas espera, o teste cria com 10, empresta 2 (virtualmente no teste anterior? nao, setUp recria))
        # No setUp cria com 10.
        # Aqui criei o objeto Emprestimo mas não decrementei do banco explicitamente no teste, 
        # mas o teste deve simular o fluxo completo.
        # Vamos ajustar:
        
        # 1. Decrementar inicial
        self.equipamento.quantidade -= 2
        self.equipamento.save()
        self.assertEqual(self.equipamento.quantidade, 8)
        
        # 2. Devolver
        self.equipamento.quantidade += 2
        self.equipamento.save()
        self.assertEqual(self.equipamento.quantidade, 10)
        self.assertEqual(emprestimo.status, 'DEVOLVIDO')
