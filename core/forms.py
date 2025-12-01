# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Colaborador, Equipamento

class LoginForm(forms.Form):
    # O widget de EmailInput garante a validação básica do formato
    # e renderiza <input type="email"> (embora seu HTML use type="text")
    # Usamos attrs para manter os IDs do seu HTML original.
    email = forms.EmailField(
        label="EMAIL :",
        widget=forms.EmailInput(attrs={'id': 'email'})
    )
    password = forms.CharField(
        label="SENHA :",
        widget=forms.PasswordInput(attrs={'id': 'password'})
    )

class RegistrationForm(forms.Form):
    email = forms.EmailField(
        label="EMAIL :",
        widget=forms.EmailInput(attrs={'id': 'email'})
    )
    password = forms.CharField(
        label="SENHA :",
        widget=forms.PasswordInput(attrs={'id': 'password'})
    )
    cf_password = forms.CharField(
        label="CONFIRMAR SENHA :",
        widget=forms.PasswordInput(attrs={'id': 'cf_password'})
    )

    def clean_email(self):
        """
        Validação para verificar se o email já existe.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Um usuário com este email já existe.")
        return email

    def clean(self):
        """
        Validação para verificar se as duas senhas coincidem.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        cf_password = cleaned_data.get("cf_password")

        if password and cf_password and password != cf_password:
            raise forms.ValidationError("As senhas não coincidem. Tente novamente.")
        
        return cleaned_data

class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ['nome', 'email','funcao'] # Campos que aparecerão no formulário
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