from django.urls import path
from . import views

app_name = 'equipamentos'

urlpatterns = [
    path('', views.app_items, name='app_items'),
    path('create/', views.app_items_create, name='app_items_create'),
    path('edit/<int:pk>/', views.app_items_edit, name='app_items_edit'),
    path('delete/<int:pk>/', views.app_items_delete, name='app_items_delete'),
]
