# urls.py
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Rotas de Login
    path('', views.login_view, name='login'),
    path('login_create', views.login_create, name='login_create'),

    #Rota de Logout
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Dashboard
    path('app/dashboard/', include('dashboard.urls')),
    
    # Users (Colaboradores)
    path('app/users/', include('colaboradores.urls')), 
    
    # Items (Equipamentos)
    path('app/items/', include('equipamentos.urls')),

    # Emprestimos (Requests)
    path('app/requests/', include('emprestimos.urls')),

    # History
    path('app/history/', include('historico.urls')),
    
    # Reports
    path('app/reports/', include('relatorios.urls')),
    
    # --- ÁREA DE CONFIGURAÇÕES ---
    path('app/configs', views.app_configs, name='app_configs'),
    
    # Rotas para Mudar Senha
    path('app/configs/senha/', 
         auth_views.PasswordChangeView.as_view(template_name='config_senha.html'), 
         name='password_change'),
         
    path('app/configs/senha/concluido/', 
         auth_views.PasswordChangeDoneView.as_view(template_name='config_senha_concluida.html'), 
         name='password_change_done'),
]