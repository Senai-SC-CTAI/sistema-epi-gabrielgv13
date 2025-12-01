from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def app_reports(request):
    return render(request, 'app_ui_reports.html')

@login_required
def app_configs(request):
    return render(request, 'app_ui_configs.html')
