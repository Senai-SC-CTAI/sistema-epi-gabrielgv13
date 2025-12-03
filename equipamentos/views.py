from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Equipamento
from .forms import EquipamentoForm

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
        'add_url_name': 'equipamentos:app_items_create',
        'edit_url_name': 'equipamentos:app_items_edit',   
        'delete_url_name': 'equipamentos:app_items_delete',
    }
    return render(request, 'app_ui_items.html', context)

@login_required
def app_items_create(request):
    if request.method == 'POST':
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            item_salvo = form.save()
            messages.success(request,  f'Equipamento "{item_salvo.nome}" cadastrado com sucesso!')
            return redirect('equipamentos:app_items')
        else:
            messages.error(request, 'Falha no cadastro. Verifique os erros abaixo.')
    else:
        form = EquipamentoForm()

    context = {
        'form': form,
        'page_title': 'Cadastrar Novo Equipamento',
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
            return redirect('equipamentos:app_items')
    else:
        form = EquipamentoForm(instance=item)

    context = {
        'form': form,
        'page_title': f'Editar Equipamento: {item.nome}',
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
        messages.success(request, 'Equipamento excluído com sucesso!')
        return redirect('equipamentos:app_items')

    context = {
        'item': item,
    }
    return render(request, 'app_ui_delete_confirm_base.html', context)
