from datetime import datetime, timedelta
import pytest
from django.test import TestCase, Client
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models

from core.utils import calculate_deadline
from core.forms import RegistrationForm, LoginForm
from equipamentos.models import Equipamento
from equipamentos.forms import EquipamentoForm
from colaboradores.models import Colaborador
from colaboradores.forms import ColaboradorForm
from emprestimos.models import Emprestimo
from emprestimos.forms import EmprestimoForm


# =====================================================
# APP: LOGIN / AUTENTICAÇÃO
# =====================================================
@pytest.mark.django_db
class LoginTestCase(TestCase):
    """Testes para funcionalidade de login e criação de conta."""
    
    def setUp(self):
        self.client = Client()
    
    # TESTE UNITÁRIO 1
    def test_unit_validacao_formulario_registro(self):
        """
        Testa a validação do formulário de registro.
        Verifica se senhas diferentes são rejeitadas.
        """
        form_data = {
            'email': 'teste@email.com',
            'password': 'senha123',
            'cf_password': 'senha456'  # Senha diferente
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('As senhas não coincidem', str(form.errors))
    
    # TESTE UNITÁRIO 2
    def test_unit_email_duplicado_bloqueado(self):
        """
        Testa se o formulário impede cadastro de email duplicado.
        """
        # Criar usuário existente
        User.objects.create_user(username='user@test.com', email='user@test.com', password='pass')
        
        # Tentar registrar com mesmo email
        form_data = {
            'email': 'user@test.com',
            'password': 'senha123',
            'cf_password': 'senha123'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    # TESTE DE INTEGRAÇÃO
    def test_integration_fluxo_completo_registro_e_login(self):
        """
        Testa o fluxo completo: criar conta -> fazer login -> acessar sistema.
        """
        # 1. Criar conta via POST
        response = self.client.post(reverse('login_create'), {
            'email': 'novo@test.com',
            'password': 'senha123',
            'cf_password': 'senha123'
        })
        
        # Verificar se usuário foi criado
        self.assertTrue(User.objects.filter(email='novo@test.com').exists())
        
        # 2. Fazer login
        login_success = self.client.login(username='novo@test.com', password='senha123')
        self.assertTrue(login_success)
        
        # 3. Tentar acessar página protegida (dashboard)
        response = self.client.get(reverse('dashboard:app_dashboard'))
        self.assertEqual(response.status_code, 200)


# =====================================================
# APP: EMPRÉSTIMOS
# =====================================================
@pytest.mark.django_db
class EmprestimosTestCase(TestCase):
    """Testes para funcionalidade de empréstimos."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test@test.com', password='pass')
        self.colaborador = Colaborador.objects.create(nome="João Silva", email="joao@test.com")
        self.equipamento = Equipamento.objects.create(nome="Capacete", marca="3M", quantidade=10)
    
    # TESTE UNITÁRIO 1
    def test_unit_validacao_quantidade_minima(self):
        """
        Testa validação de quantidade mínima no formulário de empréstimo.
        Verifica que quantidades menores que 1 são rejeitadas com mensagem apropriada.
        """
        # Testar quantidade zero
        form_data = {
            'nome': self.colaborador.id,
            'equipamento': self.equipamento.id,
            'quantidade': 0
        }
        form = EmprestimoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('A quantidade mínima para empréstimo é 1', str(form.errors))
        
        # Testar quantidade negativa
        form_data['quantidade'] = -5
        form = EmprestimoForm(data=form_data)
        self.assertFalse(form.is_valid())
        
        # Testar quantidade válida (valor de fronteira)
        form_data['quantidade'] = 1
        form = EmprestimoForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    # TESTE UNITÁRIO 2
    def test_unit_validacao_estoque_insuficiente(self):
        """
        Testa validação de estoque disponível no formulário.
        Verifica que empréstimos acima do estoque são rejeitados e que
        a mensagem informa o estoque atual disponível.
        """
        estoque_atual = self.equipamento.quantidade  # 10
        
        # Testar quantidade acima do estoque
        form_data = {
            'nome': self.colaborador.id,
            'equipamento': self.equipamento.id,
            'quantidade': estoque_atual + 5
        }
        form = EmprestimoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Quantidade indisponível', str(form.errors))
        self.assertIn(f'Estoque atual: {estoque_atual}', str(form.errors))
        
        # Testar valor limite exato (deve passar)
        form_data['quantidade'] = estoque_atual
        form = EmprestimoForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        # Testar valor um acima do limite (deve falhar)
        form_data['quantidade'] = estoque_atual + 1
        form = EmprestimoForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    # TESTE DE INTEGRAÇÃO
    def test_integration_criar_emprestimo_e_devolver(self):
        """
        Testa o fluxo completo: criar empréstimo -> atualizar estoque -> devolver -> restaurar estoque.
        """
        estoque_inicial = self.equipamento.quantidade
        
        # 1. Criar empréstimo
        emprestimo = Emprestimo.objects.create(
            nome=self.colaborador,
            equipamento=self.equipamento,
            quantidade=3,
            data_prazo=calculate_deadline(timezone.now()),
            estoque_disponivel=7,
            status='EMPRESTADO'
        )
        
        # 2. Atualizar estoque
        self.equipamento.quantidade -= emprestimo.quantidade
        self.equipamento.save()
        self.equipamento.refresh_from_db()
        self.assertEqual(self.equipamento.quantidade, 7)
        
        # 3. Devolver empréstimo
        emprestimo.status = 'DEVOLVIDO'
        emprestimo.data_devolucao_real = timezone.now()
        emprestimo.save()
        
        # 4. Restaurar estoque
        self.equipamento.quantidade += emprestimo.quantidade
        self.equipamento.save()
        self.equipamento.refresh_from_db()
        
        # Verificar se estoque voltou ao valor original
        self.assertEqual(self.equipamento.quantidade, estoque_inicial)
        self.assertEqual(emprestimo.status, 'DEVOLVIDO')


# =====================================================
# APP: EQUIPAMENTOS
# =====================================================
@pytest.mark.django_db
class EquipamentosTestCase(TestCase):
    """Testes para funcionalidade de equipamentos."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test@test.com', password='pass')
    
    # TESTE UNITÁRIO 1
    def test_unit_validacao_campos_obrigatorios(self):
        """
        Verifica se o formulário valida que todos os campos obrigatórios
        (nome, marca, quantidade) estão preenchidos.
        """
        # Testar sem nome (deve falhar)
        form_data = {
            'nome': '',
            'marca': '3M',
            'quantidade': 10
        }
        form = EquipamentoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nome', form.errors)
        
        # Testar sem marca (deve falhar)
        form_data = {
            'nome': 'Capacete',
            'marca': '',
            'quantidade': 10
        }
        form = EquipamentoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('marca', form.errors)
        
        # Testar com todos os campos (deve passar)
        form_data = {
            'nome': 'Capacete',
            'marca': '3M',
            'quantidade': 10
        }
        form = EquipamentoForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    # TESTE UNITÁRIO 2
    def test_unit_validacao_quantidade_positiva(self):
        """
        Testa se o formulário valida que apenas quantidades positivas são aceitas.
        Verifica que quantidades negativas e zero são rejeitadas.
        """
        # Testar quantidade negativa (deve falhar)
        form_data = {
            'nome': 'Capacete',
            'marca': '3M',
            'quantidade': -5
        }
        form = EquipamentoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('quantidade', form.errors)
        
        # Testar quantidade zero (deve falhar)
        form_data['quantidade'] = 0
        form = EquipamentoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('A quantidade mínima em estoque é 1.', str(form.errors))
        
        # Testar quantidade positiva válida (deve passar)
        form_data['quantidade'] = 5
        form = EquipamentoForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        # Testar valor de fronteira mínimo (1)
        form_data['quantidade'] = 1
        form = EquipamentoForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    # TESTE DE INTEGRAÇÃO
    def test_integration_crud_completo_equipamento(self):
        """
        Testa operações CRUD completas: Criar -> Ler -> Atualizar -> Deletar.
        """
        # CREATE
        equipamento = Equipamento.objects.create(
            nome="Óculos",
            marca="Vonder",
            quantidade=15
        )
        pk = equipamento.pk
        
        # READ
        equipamento_lido = Equipamento.objects.get(pk=pk)
        self.assertEqual(equipamento_lido.nome, "Óculos")
        
        # UPDATE
        equipamento_lido.quantidade = 20
        equipamento_lido.save()
        equipamento_lido.refresh_from_db()
        self.assertEqual(equipamento_lido.quantidade, 20)
        
        # DELETE
        equipamento_lido.delete()
        self.assertFalse(Equipamento.objects.filter(pk=pk).exists())


# =====================================================
# APP: COLABORADORES
# =====================================================
@pytest.mark.django_db
class ColaboradoresTestCase(TestCase):
    """Testes para funcionalidade de colaboradores."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test@test.com', password='pass')
    
    # TESTE UNITÁRIO 1
    def test_unit_email_unico(self):
        """
        Testa se o modelo garante unicidade de email.
        """
        Colaborador.objects.create(nome="Maria", email="maria@empresa.com")
        
        # Tentar criar com email duplicado deve falhar
        with self.assertRaises(Exception):
            Colaborador.objects.create(nome="João", email="maria@empresa.com")
    
    # TESTE UNITÁRIO 2
    def test_unit_email_invalido_sem_arroba(self):
        """
        Testa se o formulário rejeita emails inválidos sem o símbolo "@".
        Verifica a validação de formato de email.
        """
        # Testar email sem @ (deve falhar)
        form_data = {
            'nome': 'Pedro Santos',
            'email': 'pedroemptresa.com',
            'funcao': 'Engenheiro'
        }
        form = ColaboradorForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        
        # Testar email com @ mas sem domínio (deve falhar)
        form_data['email'] = 'pedro@'
        form = ColaboradorForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        
        # Testar email válido (deve passar)
        form_data['email'] = 'pedro@empresa.com'
        form = ColaboradorForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    # TESTE DE INTEGRAÇÃO
    def test_integration_colaborador_com_emprestimos(self):
        """
        Testa integração: criar colaborador -> associar a empréstimo -> verificar relação.
        """
        # 1. Criar colaborador
        colaborador = Colaborador.objects.create(
            nome="Ana Costa",
            email="ana@empresa.com",
            funcao="Técnica"
        )
        
        # 2. Criar equipamento
        equipamento = Equipamento.objects.create(
            nome="Bota",
            marca="Marluvas",
            quantidade=10
        )
        
        # 3. Criar empréstimo associado
        emprestimo = Emprestimo.objects.create(
            nome=colaborador,
            equipamento=equipamento,
            quantidade=2,
            data_prazo=calculate_deadline(timezone.now()),
            estoque_disponivel=8,
            status='EMPRESTADO'
        )
        
        # 4. Verificar relação
        self.assertEqual(emprestimo.nome.email, "ana@empresa.com")
        self.assertEqual(emprestimo.nome.nome, "Ana Costa")
        
        # 5. Verificar que colaborador não pode ser deletado enquanto tem empréstimo ativo
        with self.assertRaises(Exception):
            colaborador.delete()


# =====================================================
# APP: HISTÓRICO
# =====================================================
@pytest.mark.django_db
class HistoricoTestCase(TestCase):
    """Testes para funcionalidade de histórico."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test@test.com', password='pass')
        self.client.login(username='test@test.com', password='pass')
        
        self.colaborador = Colaborador.objects.create(nome="Carlos", email="carlos@test.com")
        self.equipamento = Equipamento.objects.create(nome="Luva", marca="Safety", quantidade=10)
    
    # TESTE UNITÁRIO 1
    def test_unit_emprestimo_excluido_nao_aparece_no_historico(self):
        """
        Testa se ao excluir um empréstimo, ele não aparece na aba de movimentações (histórico).
        Valida que registros deletados são removidos completamente do histórico.

        """
        # 1. Criar empréstimo
        emprestimo = Emprestimo.objects.create(
            nome=self.colaborador,
            equipamento=self.equipamento,
            quantidade=5,
            data_prazo=calculate_deadline(timezone.now()),
            estoque_disponivel=5,
            status='EMPRESTADO'
        )
        
        # 2. Atualizar estoque
        self.equipamento.quantidade -= emprestimo.quantidade
        self.equipamento.save()
        
        # 3. Devolver empréstimo
        emprestimo.status = 'DEVOLVIDO'
        emprestimo.data_devolucao_real = timezone.now()
        emprestimo.save()
        
        emprestimo_id = emprestimo.pk
        
        # 4. Verificar que aparece no histórico (queryset de devolvidos)
        historico_antes = Emprestimo.objects.filter(status='DEVOLVIDO')
        self.assertEqual(historico_antes.count(), 1)
        self.assertTrue(historico_antes.filter(pk=emprestimo_id).exists())
        
        # 5. Deletar o empréstimo
        emprestimo.delete()
        
        # 6. Verificar que NÃO aparece mais no histórico
        historico_depois = Emprestimo.objects.filter(status='DEVOLVIDO')
        self.assertEqual(historico_depois.count(), 0)
        self.assertFalse(historico_depois.filter(pk=emprestimo_id).exists())
        self.assertFalse(Emprestimo.objects.filter(pk=emprestimo_id).exists())
    
    # TESTE UNITÁRIO 2
    def test_unit_emprestimo_devolvido_aparece_no_historico(self):
        """
        s
        
        Cenário:
        - Criar empréstimo
        - Devolver empréstimo (status = DEVOLVIDO)
        - Verificar que aparece no histórico (queryset de devolvidos)
        """
        # 1. Criar empréstimo
        emprestimo = Emprestimo.objects.create(
            nome=self.colaborador,
            equipamento=self.equipamento,
            quantidade=5,
            data_prazo=calculate_deadline(timezone.now()),
            estoque_disponivel=5,
            status='EMPRESTADO'
        )
        
        # 2. Atualizar estoque
        self.equipamento.quantidade -= emprestimo.quantidade
        self.equipamento.save()
        
        # 3. Devolver empréstimo
        emprestimo.status = 'DEVOLVIDO'
        emprestimo.data_devolucao_real = timezone.now()
        emprestimo.save()
        
        emprestimo_id = emprestimo.pk
        
        # 4. Verificar que aparece no histórico (queryset de devolvidos)
        historico = Emprestimo.objects.filter(status='DEVOLVIDO')
        self.assertEqual(historico.count(), 1)
        self.assertTrue(historico.filter(pk=emprestimo_id).exists())
        self.assertEqual(historico.first().status, 'DEVOLVIDO')
    
    # TESTE DE INTEGRAÇÃO
    def test_integration_acesso_pagina_historico(self):
        """
        Testa acesso completo à página de histórico com dados reais.
        """
        # 1. Criar empréstimo devolvido
        Emprestimo.objects.create(
            nome=self.colaborador,
            equipamento=self.equipamento,
            quantidade=5,
            data_prazo=calculate_deadline(timezone.now()),
            estoque_disponivel=5,
            status='DEVOLVIDO',
            data_devolucao_real=timezone.now()
        )
        
        # 2. Acessar página de histórico
        response = self.client.get(reverse('historico:app_history'))
        
        # 3. Verificar resposta
        self.assertEqual(response.status_code, 200)
        self.assertIn('object_data', response.context)
        self.assertEqual(len(response.context['object_data']), 1)
        self.assertIn('Carlos', str(response.context['object_data']))
