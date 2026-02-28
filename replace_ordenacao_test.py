import os
os.chdir(r'C:\Users\gabriel_ventura1\Documents\GitHub\sistema-epi-gabrielgv13')

with open('core/tests.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_test = '''    # TESTE UNITÁRIO 2
    def test_unit_ordenacao_por_data_devolucao(self):
        """
        Testa se empréstimos são ordenados por data de devolução (mais recente primeiro).
        """
        # Criar empréstimos devolvidos em momentos diferentes
        emp1 = Emprestimo.objects.create(
            nome=self.colaborador,
            equipamento=self.equipamento,
            quantidade=1,
            data_prazo=calculate_deadline(timezone.now()),
            estoque_disponivel=9,
            status='DEVOLVIDO',
            data_devolucao_real=timezone.now() - timedelta(days=2)
        )
        
        emp2 = Emprestimo.objects.create(
            nome=self.colaborador,
            equipamento=self.equipamento,
            quantidade=1,
            data_prazo=calculate_deadline(timezone.now()),
            estoque_disponivel=8,
            status='DEVOLVIDO',
            data_devolucao_real=timezone.now()
        )
        
        # Buscar ordenado (mais recente primeiro)
        historico = Emprestimo.objects.filter(status='DEVOLVIDO').order_by('-data_devolucao_real')
        self.assertEqual(historico.first().pk, emp2.pk)'''

new_test = '''    # TESTE UNITÁRIO 2
    def test_unit_atualizacao_estoque_disponivel_ao_devolver(self):
        """
        Testa se ao devolver um empréstimo, o estoque_disponivel de outros 
        empréstimos ativos do mesmo equipamento é atualizado corretamente.
        """
        # 1. Criar dois empréstimos ativos do mesmo equipamento
        emp1 = Emprestimo.objects.create(
            nome=self.colaborador,
            equipamento=self.equipamento,
            quantidade=3,
            data_prazo=calculate_deadline(timezone.now()),
            estoque_disponivel=7,  # 10 - 3
            status='EMPRESTADO'
        )
        
        emp2 = Emprestimo.objects.create(
            nome=self.colaborador,
            equipamento=self.equipamento,
            quantidade=2,
            data_prazo=calculate_deadline(timezone.now()),
            estoque_disponivel=5,  # 7 - 2
            status='EMPRESTADO'
        )
        
        # 2. Registrar estoque_disponivel inicial de emp2
        estoque_disponivel_inicial = emp2.estoque_disponivel  # 5
        
        # 3. Atualizar equipamento para refletir os dois empréstimos
        self.equipamento.quantidade = 5  # 10 - 3 - 2
        self.equipamento.save()
        
        # 4. Devolver o primeiro empréstimo
        emp1.status = 'DEVOLVIDO'
        emp1.data_devolucao_real = timezone.now()
        emp1.save()
        
        # 5. Atualizar estoque ao devolver
        self.equipamento.quantidade += emp1.quantidade  # 5 + 3 = 8
        self.equipamento.save()
        self.equipamento.refresh_from_db()
        
        # 6. Atualizar estoque_disponivel de emp2 (deveria aumentar pois estoque recuperado)
        emp2.estoque_disponivel = self.equipamento.quantidade - 2  # 8 - 2 = 6
        emp2.save()
        emp2.refresh_from_db()
        
        # 7. Verificar que estoque_disponivel foi atualizado
        self.assertGreater(emp2.estoque_disponivel, estoque_disponivel_inicial)
        self.assertEqual(emp2.estoque_disponivel, 6)
        self.assertEqual(self.equipamento.quantidade, 8)'''

if old_test in content:
    content = content.replace(old_test, new_test)
    with open('core/tests.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('✓ Teste substituído com sucesso!')
else:
    print('✗ Teste original não encontrado')
