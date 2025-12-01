# views.py

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Import forms
from .forms import LoginForm, RegistrationForm

# frameworks
# Django Messages Framework
from django.contrib import messages

# --- VIEW DE LOGIN (USANDO FORM) ---
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:app_dashboard')
    
    error_message = None

    if request.method == 'POST':
        # 1. Crie uma instância do formulário
        form = LoginForm(request.POST) # Usa o LoginForm
        
        # 2. Verifique se é válido
        if form.is_valid():
            cd = form.cleaned_data
            email = cd.get('email')
            password = cd.get('password')

            try:
                user_obj = User.objects.get(email=email)
                username = user_obj.username
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    auth_login(request, user)
                    return redirect('dashboard:app_dashboard')
                else:
                    error_message = "Senha incorreta. Tente novamente."

            except User.DoesNotExist:
                error_message = "Nenhum usuário encontrado com este email."
            except Exception as e:
                error_message = f"Ocorreu um erro: {e}"
    else:
        # 3. Se for GET, crie um formulário vazio
        form = LoginForm()

    context = {'form': form, 'error': error_message}
    return render(request, "login.html", context)


# --- VIEW DE CRIAÇÃO DE CONTA (USANDO FORM) ---
def login_create(request):
    if request.user.is_authenticated:
        return redirect('dashboard:app_dashboard')

    if request.method == 'POST':
        form = RegistrationForm(request.POST) # Usa o RegistrationForm
        
        if form.is_valid():
            cd = form.cleaned_data
            email = cd.get('email')
            password = cd.get('password')

            try:
                user = User.objects.create_user(username=email, email=email, password=password)
                
                user_auth = authenticate(request, username=email, password=password)
                if user_auth is not None:
                    auth_login(request, user_auth)
                    return redirect('dashboard:app_dashboard')
                else:
                    form.add_error(None, "Erro ao autenticar após a criação.")

            except Exception as e:
                form.add_error(None, f"Ocorreu um erro inesperado: {e}")
    else:
        form = RegistrationForm()

    # O 'form' carrega todos os erros de validação
    context = {'form': form}
    return render(request, 'login_create.html', context)


# Config view - kept in core as it's simple
@login_required
def app_configs(request):
    return render(request, 'app_ui_configs.html')