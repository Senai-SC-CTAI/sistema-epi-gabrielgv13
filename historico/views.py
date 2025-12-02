from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from emprestimos.models import Emprestimo

@login_required
def app_history(request):
    """
    Mostra o histórico de todos os empréstimos devolvidos.
    """
    emprestimos_devolvidos = Emprestimo.objects.filter(status='DEVOLVIDO').order_by('-data_devolucao_real')
    
    object_data = []
    for emp in emprestimos_devolvidos:
        # Converter para timezone local antes de formatar
        data_emprestimo_local = timezone.localtime(emp.data_emprestimo)
        data_prazo_local = timezone.localtime(emp.data_prazo)
        data_devolucao_local = timezone.localtime(emp.data_devolucao_real) if emp.data_devolucao_real else None
        
        object_data.append({
            'pk': emp.pk,
            'fields': [
                emp.nome.nome,
                emp.equipamento.nome,
                emp.quantidade,
                data_emprestimo_local.strftime('%d/%m/%Y %H:%M'),
                data_prazo_local.strftime('%d/%m/%Y %H:%M'),
                data_devolucao_local.strftime('%d/%m/%Y %H:%M') if data_devolucao_local else '-',
                emp.get_status_display(),
            ]
        })
    
    context = {
        'page_title': 'Histórico de Devoluções',
        'headers': ['Colaborador', 'Equipamento', 'Quantidade', 'Data Empréstimo', 'Prazo Devolução', 'Data Devolução', 'Status'],
        'object_data': object_data,
    }
    return render(request, 'app_ui_history.html', context)
