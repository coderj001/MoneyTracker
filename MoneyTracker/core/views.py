from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    return render(request, 'core/index.html', context={})


@login_required
def add_expense(request):
    return render(request, 'core/add_expense.html', context={})
