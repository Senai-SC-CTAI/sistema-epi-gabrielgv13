from django.urls import path
from . import views

app_name = 'colaboradores'

urlpatterns = [
    path('', views.app_users, name='app_users'),
    path('create/', views.app_users_create, name='app_users_create'),
    path('edit/<int:pk>/', views.app_users_edit, name='app_users_edit'),
    path('delete/<int:pk>/', views.app_users_delete, name='app_users_delete'),
]
