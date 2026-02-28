with open('core/tests.py', 'r') as f:
    content = f.read()

# Substituir o teste
old_test = '''    # TESTE UNITÁRIO 2
    def test_unit_validacao_formulario_colaborador(self):
        """
        Testa validação do formulário de colaborador.
        """
        form_data = {
            'nome': 'Pedro Santos',
            'email': 'pedro@empresa.com',
            'funcao': 'Engenheiro'
        }
        form = ColaboradorForm(data=form_data)
        self.assertTrue(form.is_valid())'''

new_test = '''    # TESTE UNITÁRIO 2
    def test_unit_email_invalido_sem_arroba(self):
        """
        Testa se o formulário rejeita emails inválidos sem o símbolo "@".
        Verifica a validação de formato de email.
        """
        # Testar email sem @ (deve falhar)
        form_data = {
            'nome': 'Pedro Santos',
            'email': 'pedroemptresa.com',  # Falta o @
            'funcao': 'Engenheiro'
        }
        form = ColaboradorForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        
        # Testar email vazio (deve falhar)
        form_data['email'] = ''
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
        self.assertTrue(form.is_valid())'''

content = content.replace(old_test, new_test)

with open('core/tests.py', 'w') as f:
    f.write(content)

print('✓ Teste substituído com sucesso!')
