import csv
import json
from tempfile import NamedTemporaryFile

import xlwt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.timezone import localtime, now, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from expenses.models import Catagory, Expense
from weasyprint import HTML


@login_required(login_url=reverse_lazy('auth:login'))
def home_expense(request: HttpRequest) -> HttpResponse:
    data = Expense.objects.filter(owner=request.user)
    paginator = Paginator(data, 6)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    return render(request, 'expenses/index.html',
                  context={"page_obj": page_obj})


@login_required(login_url=reverse_lazy('auth:login'))
def add_expense(request: HttpRequest) -> HttpResponse:
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
def edit_expense(request: HttpRequest, id: int) -> HttpResponse:
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
def delete_expense(request: HttpRequest, id: int) -> HttpResponse:
    expense = Expense.objects.get(pk=id)
    expense.delete()
    return redirect('expenses:home-expense')


@csrf_exempt
@require_POST
@login_required
def search_expenses(request: HttpRequest) -> HttpResponse:
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
def expense_category_summery(request: HttpRequest) -> HttpResponse:
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
def expense_summery(request: HttpRequest) -> HttpResponse:
    return render(request, 'expenses/expenses_summery.html')


@login_required
def export_csv(request: HttpRequest) -> HttpResponse:
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; ' \
        f'filename=Expenses-{request.user.username}-{now().date()}.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Catagory', 'Date'])

    expenses = Expense.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.amount, expense.description,
                         expense.category, expense.date])

    return response


@login_required
def export_excel(request: HttpRequest) -> HttpResponse:
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; ' \
        f'filename=Expenses-{request.user.username}-{now().date()}.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Amount', 'Description', 'Catagory', 'Date']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    rows = Expense.objects.filter(owner=request.user).values_list(
        'amount', 'description', 'category', 'date')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)
    return response


@login_required
def export_pdf(request: HttpRequest) -> HttpResponse:
    response = HttpResponse(content_type='application/pfd')
    response['Content-Disposition'] = 'inlineattachment; ' \
        f'filename=Expenses-{request.user.username}-{now().date()}.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    expenses = Expense.objects.filter(owner=request.user)

    sum = expenses.aggregate(Sum('amount')).get('amount__sum')

    html_string = render_to_string(
        'expenses/pdf-output.html',
        {'expenses': expenses,
         'total': sum})

    html = HTML(string=html_string)
    result = html.write_pdf()

    with NamedTemporaryFile(delete=True) as output:

        output.write(result)
        output.flush()

        output = open(output.name, 'rb')
        response.write(output.read())

    return response
