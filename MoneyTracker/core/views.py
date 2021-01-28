from core.models import Catagory, Expense
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.timezone import now


@login_required(login_url=reverse_lazy('auth:login'))
def home(request):
    data = Expense.objects.filter(owner=request.user)
    return render(request, 'core/index.html', context={"expenses": data})


@login_required(login_url=reverse_lazy('auth:login'))
def add_expense(request):
    catagory = Catagory.objects.all()

    if request.method == 'POST':
        amount = request.POST.get('amount')
        if not amount:
            messages.add_message(request, messages.WARNING,
                                 "Amount is required.")
            return render(request, 'core/add_expense.html',
                          context={'catagories': catagory,
                                   'fieldVal': request.POST}
                          )

        description = request.POST.get('description')
        catagory_res = request.POST.get('catagory')
        # ERROR:  <29-01-21, coderj001> # catagory not working
        date = request.POST.get('date')
        if not date:
            date = now().date()
        Expense.objects.create(owner=request.user,
                               amount=amount, description=description,
                               category=catagory_res, date=date)
        messages.add_message(request, messages.SUCCESS,
                             "Expense saved successfully.")
        return redirect('core:home')

    return render(request, 'core/add_expense.html',
                  context={'catagories': catagory}
                  )
