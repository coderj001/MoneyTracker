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
from django.urls import reverse_lazy
from django.utils.timezone import localtime, now, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from income.models import Income, Source
from weasyprint import HTML


@login_required(login_url=reverse_lazy('auth:login'))
def home_income(request: HttpRequest) -> HttpResponse:
    data = Income.objects.filter(owner=request.user)
    paginator = Paginator(data, 6)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    return render(request, 'income/index.html',
                  context={"page_obj": page_obj})


@login_required(login_url=reverse_lazy('auth:login'))
def add_income(request: HttpRequest) -> HttpResponse:
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
def edit_income(request: HttpRequest, id: int) -> HttpResponse:
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
def delete_income(request: HttpRequest, id: int) -> HttpResponse:
    income = Income.objects.get(pk=id)
    income.delete()
    return redirect('income:home-income')


@csrf_exempt
@require_POST
@login_required
def search_income(request: HttpRequest) -> HttpResponse:
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


@csrf_exempt
@login_required
def income_source_summery(request: HttpRequest) -> HttpResponse:
    todays_date = localtime()
    six_months_ago = todays_date-timedelta(days=30*6)
    income = Income.objects.filter(
        owner=request.user, date__gte=six_months_ago, date__lte=todays_date)
    source_list = income.values_list('source', flat=True).distinct()

    source_price = dict()
    for source in source_list:
        source_price[source] = income.filter(
            source=source).aggregate(Sum('amount')).get('amount__sum')

    return JsonResponse({'income_source_data': source_price},
                        safe=False)


@login_required
def income_summery(request: HttpRequest) -> HttpResponse:
    return render(request, 'income/income_summery.html')


@login_required
def income_csv(request: HttpRequest) -> HttpResponse:
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; ' \
        f'filename=Income-{request.user.username}-{now().date()}.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Source', 'Date'])

    incomes = Income.objects.filter(owner=request.user)

    for income in incomes:
        writer.writerow([income.amount, income.description,
                         income.source, income.date])

    return response


@login_required
def export_excel(request: HttpRequest) -> HttpResponse:
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; ' \
        f'filename=Income-{request.user.username}-{now().date()}.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Income')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Amount', 'Description', 'Source', 'Date']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    rows = Income.objects.filter(owner=request.user).values_list(
        'amount', 'description', 'source', 'date')
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
        f'filename=Income-{request.user.username}-{now().date()}.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    incomes = Income.objects.filter(owner=request.user)

    sum = incomes.aggregate(Sum('amount')).get('amount__sum')

    html_string = render_to_string(
        'incomes/pdf-output.html',
        {'incomes': incomes,
         'total': sum})

    html = HTML(string=html_string)
    result = html.write_pdf()

    with NamedTemporaryFile(delete=True) as output:

        output.write(result)
        output.flush()

        output = open(output.name, 'rb')
        response.write(output.read())

    return response
