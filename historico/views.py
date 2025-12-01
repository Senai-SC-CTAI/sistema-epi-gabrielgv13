from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def app_history(request):
    return render(request, 'app_ui_history.html')
