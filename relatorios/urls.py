from django.urls import path
from . import views

app_name = 'relatorios'

urlpatterns = [
    path('', views.app_reports, name='app_reports'),
    path('configs/', views.app_configs, name='app_configs'),
    path('download/movimentacoes-csv/', views.download_movimentacoes_csv, name='download_movimentacoes_csv'),
]
