from django import forms
from .models import Equipamento

class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ['nome', 'marca', 'quantidade']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Capacete'}),
            'marca': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: 3M'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-input', 'min': '0'}),
        }
        labels = {
            'nome': 'Nome do Equipamento',
            'marca': 'Marca',
            'quantidade': 'Quantidade em Estoque',
        }
