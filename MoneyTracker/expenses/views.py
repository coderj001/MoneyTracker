import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.timezone import now, localtime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from expenses.models import Catagory, Expense


@login_required(login_url=reverse_lazy('auth:login'))
def home_expense(request):
    data = Expense.objects.filter(owner=request.user)
    paginator = Paginator(data, 6)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    return render(request, 'expenses/index.html',
                  context={"page_obj": page_obj})


@login_required(login_url=reverse_lazy('auth:login'))
def add_expense(request):
    catagory = Catagory.objects.all()

    if request.method == 'POST':
        amount = request.POST.get('amount')
        if not amount:
            messages.add_message(request, messages.WARNING,
                                 "Amount is required.")
            return render(request, 'expenses/add_expense.html',
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
        return redirect('expenses:home-expense')

    return render(request, 'expenses/add_expense.html',
                  context={'catagories': catagory}
                  )


@login_required(login_url=reverse_lazy('auth:login'))
def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    catagory = Catagory.objects.all()
    if request.method == 'GET':
        return render(request, 'expenses/edit_expense.html', context={
            'fieldVal': expense,
            'catagories': catagory,
        })

    if request.method == 'POST':
        amount = request.POST.get('amount')
        if not amount:
            messages.add_message(request, messages.WARNING,
                                 "Amount is required.")
            return redirect('expenses:edit-expense', id=expense.pk)

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
        return redirect('expenses:edit-expense', id=expense.pk)


@login_required(login_url=reverse_lazy('auth:login'))
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    return redirect('expenses:home-expense')


@csrf_exempt
@require_POST
@login_required
def search_expenses(request):
    if request.method == 'POST':
        search_var = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            Q(amount__startswith=search_var) |
            Q(date__startswith=search_var) |
            Q(description__icontains=search_var) |
            Q(category__icontains=search_var),
            owner=request.user)[:6]

        data = expenses.values()

        return JsonResponse(list(data), safe=False)


@csrf_exempt
@login_required
def expense_category_summery(request):
    todays_date = localtime()
    six_months_ago = todays_date-timedelta(days=30*6)
    expenses = Expense.objects.filter(
        owner=request.user, date__gte=six_months_ago, date__lte=todays_date)
    category_list = expenses.values_list('category', flat=True).distinct()

    category_price = dict()
    for category in category_list:
        category_price[category] = expenses.filter(
            category=category).aggregate(Sum('amount')).get('amount__sum')

    return JsonResponse({'expense_category_data': category_price},
                        safe=False)


@login_required
def expense_summery(request):
    return render(request, 'expenses/expenses_summery.html')
