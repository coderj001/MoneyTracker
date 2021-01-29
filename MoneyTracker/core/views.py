from core.models import Catagory, Expense
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.core.paginator import Paginator


@login_required(login_url=reverse_lazy('auth:login'))
def home(request):
    data = Expense.objects.filter(owner=request.user)
    paginator = Paginator(data, 3)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    return render(request, 'core/index.html',
                  context={"expenses": data, "page_obj": page_obj})


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
        catagory_res = request.POST.get('category')
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


@login_required(login_url=reverse_lazy('auth:login'))
def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    catagory = Catagory.objects.all()
    if request.method == 'GET':
        return render(request, 'core/edit_expense.html', context={
            'fieldVal': expense,
            'catagories': catagory,
        })

    if request.method == 'POST':
        amount = request.POST.get('amount')
        if not amount:
            messages.add_message(request, messages.WARNING,
                                 "Amount is required.")
            return redirect('core:edit-expense', id=expense.pk)

        description = request.POST.get('description')
        catagory_res = request.POST.get('category')
        date = request.POST.get('date')
        if not date:
            date = now().date()
        expense.amount = amount
        expense.description = description
        expense.category = catagory_res
        expense.date = date
        expense.save()
        messages.add_message(request, messages.SUCCESS,
                             "Expense is updated successfully.")
        return redirect('core:edit-expense', id=expense.pk)


@login_required(login_url=reverse_lazy('auth:login'))
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    return redirect('core:home')
