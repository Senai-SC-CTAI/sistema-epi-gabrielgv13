# views.py

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# --- IMPORTS CORRIGIDOS ---
# Importa os modelos
from .models import Colaborador, Equipamento 
# Importa TODOS os formulários que vamos usar
from .forms import LoginForm, RegistrationForm, ColaboradorForm, EquipamentoForm

# frameworks
# Django Messages Framework
from django.contrib import messages

# --- VIEW DE LOGIN (USANDO FORM) ---
def login_view(request):
    if request.user.is_authenticated:
        return redirect('app_dashboard')
    
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
                    return redirect('app_dashboard')
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
        return redirect('app_dashboard')

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
                    return redirect('app_dashboard')
                else:
                    form.add_error(None, "Erro ao autenticar após a criação.")

            except Exception as e:
                form.add_error(None, f"Ocorreu um erro inesperado: {e}")
    else:
        form = RegistrationForm()

    # O 'form' carrega todos os erros de validação
    context = {'form': form}
    return render(request, 'login_create.html', context)


@login_required
def app_dashboard(request):
    return render(request, 'app_ui_dashboard.html')

# --- CRUD DE COLABORADORES ---

@login_required
def app_users(request):
    """
    READ (List): Mostra todos os colaboradores.
    """
    colaboradores = Colaborador.objects.all().order_by('nome')
    
    object_data = []
    for col in colaboradores:
        object_data.append({
            'pk': col.pk,
            'fields': [col.nome, col.email, col.funcao]
        })

    context = {
        'page_title': 'Colaboradores',
        'headers': ['Nome', 'Email', 'Função'],
        'object_data': object_data,
        'add_url_name': 'app_users_create',
        'edit_url_name': 'app_users_edit',   
        'delete_url_name': 'app_users_delete',
        'active_nav': 'users'
    }
    return render(request, 'app_ui_users.html', context) #

@login_required
def app_users_create(request):
    if request.method == 'POST':
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            colaborador_salvo = form.save()
            messages.success(request, f'Colaborador "{colaborador_salvo.nome}" cadastrado com sucesso!')
            # SEM 'redirect' e SEM 'form = ColaboradorForm()'
        else:
            messages.error(request, 'Falha no cadastro. Verifique os erros abaixo.')
    else:
        form = ColaboradorForm()
    
    context = {
        'form': form, # O 'form' (preenchido ou vazio) é enviado para o template
        'page_title': 'Cadastrar Novo Colaborador',
        'active_nav': 'users'
    }
    return render(request, 'app_ui_form_base.html', context)

@login_required
def app_users_edit(request, pk):
    """
    UPDATE: Edita um colaborador existente.
    """
    colaborador = get_object_or_404(Colaborador, pk=pk)

    if request.method == 'POST':
        form = ColaboradorForm(request.POST, instance=colaborador)
        if form.is_valid():
            form.save()
            return redirect('app_users')
    else:
        form = ColaboradorForm(instance=colaborador)

    context = {
        'form': form,
        'page_title': f'Editar Colaborador: {colaborador.nome}'
    }
    # Usa o template de formulário genérico
    return render(request, 'app_ui_form_base.html', context)

@login_required
def app_users_delete(request, pk):
    """
    DELETE: Exclui um colaborador.
    """
    colaborador = get_object_or_404(Colaborador, pk=pk)

    if request.method == 'POST':
        colaborador.delete()
        return redirect('app_users')

    # --- CORREÇÃO AQUI ---
    # Passa o 'item' para o template de deleção genérico
    context = {
        'item': colaborador,
        'active_nav': 'users' 
    }
    # Usa o template de deleção genérico
    return render(request, 'app_ui_delete_confirm_base.html', context)


# --- CRUD DE EQUIPAMENTOS ---

@login_required
def app_items(request):
    """
    READ (List): Mostra todos os equipamentos.
    """
    equipamentos = Equipamento.objects.all().order_by('nome')
    
    object_data = []
    for item in equipamentos:
        object_data.append({
            'pk': item.pk,
            'fields': [item.nome, item.marca, item.quantidade]
        })

    context = {
        'page_title': 'Equipamentos',
        'headers': ['Nome', 'Marca', 'Quantidade'],
        'object_data': object_data,
        'add_url_name': 'app_items_create',
        'edit_url_name': 'app_items_edit',   
        'delete_url_name': 'app_items_delete',
        'active_nav': 'items' 
    }
    return render(request, 'app_ui_items.html', context)

@login_required
def app_items_create(request):
    if request.method == 'POST':
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            item_salvo = form.save()
            messages.success(request, f'Equipamento "{item_salvo.nome}" cadastrado com sucesso!')
            # SEM 'redirect' e SEM 'form = EquipamentoForm()'
        else:
            messages.error(request, 'Falha no cadastro. Verifique os erros abaixo.')
    else:
        form = EquipamentoForm()

    context = {
        'form': form,
        'page_title': 'Cadastrar Novo Equipamento',
        'active_nav': 'items'
    }
    return render(request, 'app_ui_form_base.html', context)

    context = {
        'form': form,
        'page_title': 'Cadastrar Novo Equipamento',
        'active_nav': 'items'
    }
    return render(request, 'app_ui_form_base.html', context)

@login_required
def app_items_edit(request, pk):
    """
    UPDATE: Edita um equipamento existente.
    """
    item = get_object_or_404(Equipamento, pk=pk)

    if request.method == 'POST':
        form = EquipamentoForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('app_items')
    else:
        form = EquipamentoForm(instance=item)

    context = {
        'form': form,
        'page_title': f'Editar Equipamento: {item.nome}',
        'active_nav': 'items'
    }
    return render(request, 'app_ui_form_base.html', context)

@login_required
def app_items_delete(request, pk):
    """
    DELETE: Exclui um equipamento.
    """
    item = get_object_or_404(Equipamento, pk=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('app_items')

    context = {
        'item': item,
        'active_nav': 'items'
    }
    return render(request, 'app_ui_delete_confirm_base.html', context)


# --- OUTRAS VIEWS DO APP ---

@login_required
def app_requests(request):
    return render(request, 'app_ui_requests.html')

@login_required
def app_history(request):
    return render(request, 'app_ui_history.html')

@login_required
def app_reports(request):
    return render(request, 'app_ui_reports.html')

@login_required
def app_configs(request):
    return render(request, 'app_ui_configs.html')