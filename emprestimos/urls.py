from django.urls import path
from . import views

app_name = 'emprestimos'

urlpatterns = [
    path('', views.app_requests, name='app_requests'),
    path('create/', views.app_requests_create, name='app_requests_create'),
    path('edit/<int:pk>/', views.app_requests_edit, name='app_requests_edit'),
    path('delete/<int:pk>/', views.app_requests_delete, name='app_requests_delete'),
    path('return/<int:pk>/', views.app_requests_return, name='app_requests_return'),
]
