from django import forms
from .models import Equipamento

class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ['nome', 'marca', 'quantidade']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Capacete'}),
            'marca': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: 3M'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-input', 'min': '1'}),
        }
        labels = {
            'nome': 'Nome do Equipamento',
            'marca': 'Marca',
            'quantidade': 'Quantidade em Estoque',
        }

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        if quantidade is None or quantidade < 1:
            raise forms.ValidationError('A quantidade mínima em estoque é 1.')
        return quantidade
