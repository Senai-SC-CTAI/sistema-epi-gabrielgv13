from django import forms
from .models import Emprestimo

class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['nome', 'equipamento', 'quantidade']
        widgets = {
            'nome': forms.Select(attrs={'class': 'form-input'}),
            'equipamento': forms.Select(attrs={'class': 'form-input', 'id': 'id_equipamento'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-input', 'min': '1'}),
        }
        labels = {
            'nome': 'Colaborador',
            'equipamento': 'Equipamento',
            'quantidade': 'Quantidade Emprestada',
        }

    def clean(self):
        cleaned_data = super().clean()
        equipamento = cleaned_data.get('equipamento')
        quantidade = cleaned_data.get('quantidade')

        if equipamento and quantidade:
            if quantidade > equipamento.quantidade:
                raise forms.ValidationError(f"Quantidade indisponível. Estoque atual: {equipamento.quantidade}")
            
            # Calcular estoque restante para salvar no modelo (snapshot)
            self.instance.estoque_disponivel = equipamento.quantidade - quantidade

        return cleaned_data
