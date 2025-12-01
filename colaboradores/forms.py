from django import forms
from .models import Colaborador

class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ['nome', 'email','funcao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'email@empresa.com'}),
            'funcao': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Função'}),
        }
        labels = {
            'nome': 'Nome do Colaborador',
            'email': 'Email Profissional',
            'funcao': 'Função do Colaborador',
        }
