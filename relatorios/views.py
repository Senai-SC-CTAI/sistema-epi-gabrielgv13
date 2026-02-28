import csv

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from emprestimos.models import Emprestimo

@login_required
def app_reports(request):
    return render(request, 'app_ui_reports.html')

@login_required
def app_configs(request):
    return render(request, 'app_ui_configs.html')


@login_required
def download_movimentacoes_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="movimentacoes_emprestimos.csv"'
    response.write('\ufeff')

    writer = csv.writer(response)
    writer.writerow([
        'ID',
        'Colaborador',
        'Equipamento',
        'Quantidade',
        'Data Empréstimo',
        'Data Prazo',
        'Data Devolução Real',
        'Estoque Disponível',
        'Status',
    ])

    movimentacoes = Emprestimo.objects.select_related('nome', 'equipamento').order_by('-data_emprestimo')

    for movimentacao in movimentacoes:
        data_emprestimo = timezone.localtime(movimentacao.data_emprestimo).strftime('%d/%m/%Y %H:%M')
        data_prazo = timezone.localtime(movimentacao.data_prazo).strftime('%d/%m/%Y %H:%M')
        data_devolucao_real = ''

        if movimentacao.data_devolucao_real:
            data_devolucao_real = timezone.localtime(movimentacao.data_devolucao_real).strftime('%d/%m/%Y %H:%M')

        writer.writerow([
            movimentacao.pk,
            movimentacao.nome.nome,
            movimentacao.equipamento.nome,
            movimentacao.quantidade,
            data_emprestimo,
            data_prazo,
            data_devolucao_real,
            movimentacao.estoque_disponivel,
            movimentacao.get_status_display(),
        ])

    return response
