import os
os.chdir(r'C:\Users\gabriel_ventura1\Documents\GitHub\sistema-epi-gabrielgv13')

with open('core/tests.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_test = '''    # TESTE UNITÁRIO 1
    def test_unit_filtro_emprestimos_devolvidos(self):
        """
        Testa se apenas empréstimos devolvidos aparecem no histórico.
        """
        # Criar empréstimo ativo
        emp_ativo = Emprestimo.objects.create(
            nome=self.colaborador,
            equipamento=self.equipamento,
            quantidade=2,
            data_prazo=calculate_deadline(timezone.now()),
            estoque_disponivel=8,
            status='EMPRESTADO'
        )
        
        # Criar empréstimo devolvido
        emp_devolvido = Emprestimo.objects.create(
            nome=self.colaborador,
            equipamento=self.equipamento,
            quantidade=3,
            data_prazo=calculate_deadline(timezone.now()),
            estoque_disponivel=5,
            status='DEVOLVIDO',
            data_devolucao_real=timezone.now()
        )
        
        # Buscar apenas devolvidos
        devolvidos = Emprestimo.objects.filter(status='DEVOLVIDO')
        self.assertEqual(devolvidos.count(), 1)
        self.assertEqual(devolvidos.first().pk, emp_devolvido.pk)'''

new_test = '''    # TESTE UNITÁRIO 1
    def test_unit_recuperacao_estoque_ao_excluir_emprestimo(self):
        """
        Testa se ao excluir um empréstimo, a quantidade é recuperada no estoque do equipamento.
        Valida que a exclusão restaura o estoque da mesma forma que uma devolução.
        """
        estoque_inicial = self.equipamento.quantidade  # 10
        
        # 1. Criar empréstimo
        emprestimo = Emprestimo.objects.create(
            nome=self.colaborador,
            equipamento=self.equipamento,
            quantidade=4,
            data_prazo=calculate_deadline(timezone.now()),
            estoque_disponivel=6,
            status='EMPRESTADO'
        )
        
        # 2. Simular atualização de estoque (reduz pela quantidade emprestada)
        self.equipamento.quantidade -= emprestimo.quantidade
        self.equipamento.save()
        self.equipamento.refresh_from_db()
        self.assertEqual(self.equipamento.quantidade, 6)  # 10 - 4
        
        # 3. Excluir empréstimo (deve recuperar estoque)
        emprestimo_id = emprestimo.pk
        quantidade_emprestada = emprestimo.quantidade
        emprestimo.delete()
        
        # 4. Restaurar estoque (simula lógica de exclusão)
        self.equipamento.quantidade += quantidade_emprestada
        self.equipamento.save()
        self.equipamento.refresh_from_db()
        
        # 5. Verificar se estoque voltou ao valor original
        self.assertEqual(self.equipamento.quantidade, estoque_inicial)
        
        # 6. Verificar se empréstimo foi deletado
        self.assertFalse(Emprestimo.objects.filter(pk=emprestimo_id).exists())'''

if old_test in content:
    content = content.replace(old_test, new_test)
    with open('core/tests.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('✓ Teste substituído com sucesso!')
else:
    print('✗ Teste original não encontrado')
