import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from income.models import Income, Source


@login_required(login_url=reverse_lazy('auth:login'))
def home_income(request):
    data = Income.objects.filter(owner=request.user)
    paginator = Paginator(data, 6)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    return render(request, 'income/index.html',
                  context={"page_obj": page_obj})


@login_required(login_url=reverse_lazy('auth:login'))
def add_income(request):
    source = Source.objects.all()

    if request.method == 'POST':
        amount = request.POST.get('amount')
        if not amount:
            messages.add_message(request, messages.WARNING,
                                 "Amount is required.")
            return render(request, 'income/add_income.html',
                          context={'sources': source,
                                   'fieldVal': request.POST}
                          )

        description = request.POST.get('description')
        source_res = request.POST.get('source')
        date = request.POST.get('date')
        if not date:
            date = now().date()
        Income.objects.create(owner=request.user,
                              amount=amount, description=description,
                              source=source_res, date=date)
        messages.add_message(request, messages.SUCCESS,
                             "Income saved successfully.")
        return redirect('income:home-income')

    return render(request, 'income/add_income.html',
                  context={'sources': source}
                  )


@login_required(login_url=reverse_lazy('auth:login'))
def edit_income(request, id):
    income = Income.objects.get(pk=id)
    source = Source.objects.all()
    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context={
            'fieldVal': income,
            'sources': source,
        })

    if request.method == 'POST':
        amount = request.POST.get('amount')
        if not amount:
            messages.add_message(request, messages.WARNING,
                                 "Amount is required.")
            return redirect('income:edit-income', id=income.pk)

        description = request.POST.get('description')
        source_res = request.POST.get('source')
        date = request.POST.get('date')
        if not date:
            date = now().date()
        income.amount = amount
        income.description = description
        income.source = source_res
        income.date = date
        income.save()
        messages.add_message(request, messages.SUCCESS,
                             "Income is updated successfully.")
        return redirect('income:edit-income', id=income.pk)


@login_required(login_url=reverse_lazy('auth:login'))
def delete_income(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    return redirect('income:home-income')


@csrf_exempt
@require_POST
@login_required
def search_income(request):
    if request.method == 'POST':
        search_var = json.loads(request.body).get('searchText')
        income = Income.objects.filter(
            Q(amount__startswith=search_var) |
            Q(date__startswith=search_var) |
            Q(description__icontains=search_var) |
            Q(source__icontains=search_var),
            owner=request.user)[:6]

        data = income.values()

        return JsonResponse(list(data), safe=False)
