# urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Rotas de Login
    path('', views.login_view, name='login'),
    path('login_create', views.login_create, name='login_create'),

    #Rota de Logout
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    path('app/dashboard', views.app_dashboard, name='app_dashboard'),

    # Users
    path('app/users', views.app_users, name='app_users'), 
    path('app/users/create/', views.app_users_create, name='app_users_create'),
    path('app/users/edit/<int:pk>/', views.app_users_edit, name='app_users_edit'),
    path('app/users/delete/<int:pk>/', views.app_users_delete, name='app_users_delete'),
    
    # Items
    path('app/items', views.app_items, name='app_items'),
    path('app/items/create/', views.app_items_create, name='app_items_create'),
    path('app/items/edit/<int:pk>/', views.app_items_edit, name='app_items_edit'),
    path('app/items/delete/<int:pk>/', views.app_items_delete, name='app_items_delete'),

    # Outras rotas
    path('app/requests', views.app_requests, name='app_requests'),
    path('app/history', views.app_history, name='app_history'),
    path('app/reports', views.app_reports, name='app_reports'),
    
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