from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from income.models import Income, Source
from django.core.paginator import Paginator


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
        return redirect('expenses:home-income')

    return render(request, 'income/add_income.html',
                  context={'sources': source}
                  )
