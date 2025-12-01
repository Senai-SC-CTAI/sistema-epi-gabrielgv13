from django.urls import path
from . import views

app_name = 'historico'

urlpatterns = [
    path('', views.app_history, name='app_history'),
]
