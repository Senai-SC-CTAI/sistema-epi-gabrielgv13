from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Colaborador
from .forms import ColaboradorForm

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
        'add_url_name': 'colaboradores:app_users_create',
        'edit_url_name': 'colaboradores:app_users_edit',   
        'delete_url_name': 'colaboradores:app_users_delete',
    }
    return render(request, 'app_ui_users.html', context)

@login_required
def app_users_create(request):
    if request.method == 'POST':
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            colaborador_salvo = form.save()
            messages.success(request, f'Colaborador "{colaborador_salvo.nome}" cadastrado com sucesso!')
            return redirect('colaboradores:app_users')
        else:
            messages.error(request, 'Falha no cadastro. Verifique os erros abaixo.')
    else:
        form = ColaboradorForm()
    
    context = {
        'form': form,
        'page_title': 'Cadastrar Novo Colaborador',
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
            return redirect('colaboradores:app_users')
    else:
        form = ColaboradorForm(instance=colaborador)

    context = {
        'form': form,
        'page_title': f'Editar Colaborador: {colaborador.nome}'
    }
    return render(request, 'app_ui_form_base.html', context)

@login_required
def app_users_delete(request, pk):
    """
    DELETE: Exclui um colaborador.
    """
    colaborador = get_object_or_404(Colaborador, pk=pk)

    if request.method == 'POST':
        colaborador.delete()
        return redirect('colaboradores:app_users')

    context = {
        'item': colaborador,
    }
    return render(request, 'app_ui_delete_confirm_base.html', context)
