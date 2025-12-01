from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Emprestimo
from equipamentos.models import Equipamento
from .forms import EmprestimoForm
from .utils import calculate_deadline
import json

@login_required
def app_requests(request):
    """
    READ (List): Mostra todos os empréstimos.
    """
    emprestimos = Emprestimo.objects.all().order_by('-data_emprestimo')
    
    object_data = []
    for emp in emprestimos:
        object_data.append({
            'pk': emp.pk,
            'status': emp.status,
            'fields': [
                emp.nome.nome, 
                emp.equipamento.nome, 
                emp.quantidade,
                emp.data_emprestimo.strftime('%d/%m/%Y %H:%M'),
                emp.data_prazo.strftime('%d/%m/%Y %H:%M'),
                emp.estoque_disponivel,
                emp.get_status_display(), # Status
            ]
        })

    context = {
        'page_title': 'Empréstimos',
        'headers': ['Colaborador', 'Equipamento', 'Quantidade', 'Data Empréstimo', 'Prazo Devolução', 'Estoque Disponível', 'Status'],
        'object_data': object_data,
        'add_url_name': 'emprestimos:app_requests_create',
        'edit_url_name': 'emprestimos:app_requests_edit',   
        'delete_url_name': 'emprestimos:app_requests_delete',
        'return_url_name': 'emprestimos:app_requests_return',
    }
    return render(request, 'app_ui_requests.html', context)

@login_required
def app_requests_create(request):
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            emprestimo = form.save(commit=False)
            
            # Calcular data de prazo
            emprestimo.data_prazo = calculate_deadline(timezone.now())
            
            # Salvar empréstimo
            emprestimo.save()
            
            # Atualizar estoque do equipamento
            equipamento = emprestimo.equipamento
            equipamento.quantidade -= emprestimo.quantidade
            equipamento.save()
            
            messages.success(request, f'Empréstimo para "{emprestimo.nome.nome}" cadastrado com sucesso!')
            return redirect('emprestimos:app_requests')
        else:
            messages.error(request, 'Falha no cadastro. Verifique os erros abaixo.')
    else:
        form = EmprestimoForm()
    
    # Preparar dados para o JS (Estoque dinâmico)
    equipamentos_data = {eq.id: eq.quantidade for eq in Equipamento.objects.all()}
    
    context = {
        'form': form,
        'page_title': 'Cadastrar Novo Empréstimo',
        'equipamentos_json': json.dumps(equipamentos_data),
    }
    return render(request, 'app_ui_requests_create.html', context)

@login_required
def app_requests_edit(request, pk):
    """
    UPDATE: Edita um empréstimo existente.
    """
    emprestimo = get_object_or_404(Emprestimo, pk=pk)

    if request.method == 'POST':
        form = EmprestimoForm(request.POST, instance=emprestimo)
        if form.is_valid():
            form.save()
            messages.success(request, f'Empréstimo atualizado com sucesso!')
            return redirect('emprestimos:app_requests')
        else:
            messages.error(request, 'Falha ao atualizar. Verifique os erros abaixo.')
    else:
        form = EmprestimoForm(instance=emprestimo)

    context = {
        'form': form,
        'page_title': f'Editar Empréstimo',
    }
    return render(request, 'app_ui_form_base.html', context)

@login_required
def app_requests_delete(request, pk):
    """
    DELETE: Exclui um empréstimo.
    """
    emprestimo = get_object_or_404(Emprestimo, pk=pk)

    if request.method == 'POST':
        emprestimo.delete()
        messages.success(request, 'Empréstimo excluído com sucesso!')
        return redirect('emprestimos:app_requests')

    context = {
        'item': emprestimo,
    }
    return render(request, 'app_ui_delete_confirm_base.html', context)

@login_required
def app_requests_return(request, pk):
    """
    ACTION: Devolve um empréstimo.
    """
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    
    if request.method == 'POST':
        if emprestimo.status == 'EMPRESTADO':
            # Atualizar status e data
            emprestimo.status = 'DEVOLVIDO'
            emprestimo.data_devolucao_real = timezone.now()
            emprestimo.save()
            
            # Devolver ao estoque
            equipamento = emprestimo.equipamento
            equipamento.quantidade += emprestimo.quantidade
            equipamento.save()
            
            messages.success(request, f'Empréstimo devolvido com sucesso! Estoque atualizado.')
        else:
            messages.warning(request, 'Este empréstimo já foi devolvido.')
            
        return redirect('emprestimos:app_requests')

    # Se for GET, mostra confirmação
    context = {
        'item': emprestimo,
        'page_title': 'Confirmar Devolução'
    }
    return render(request, 'app_ui_return_confirm.html', context)
