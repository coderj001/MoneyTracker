from django.urls import path
from expenses.views import (add_expense, delete_expense, edit_expense,
                            expense_category_summery, expense_summery,
                            export_csv, export_excel, export_pdf, home_expense,
                            search_expenses)

app_name = 'expenses'

urlpatterns = [
    path('', home_expense, name="home-expense"),
    path('add_expense', add_expense, name="add-expense"),
    path('search_expenses', search_expenses, name="search-expenses"),
    path('expense_summery', expense_summery,
         name="expense-summery"),
    path('expense_category_summery', expense_category_summery,
         name="expense-category-summery"),
    path('export_csv', export_csv, name="export-csv"),
    path('export_excel', export_excel, name="export-excel"),
    path('export_pdf', export_pdf, name="export-pdf"),
    path('edit_expense/<int:id>/', edit_expense, name="edit-expense"),
    path('delete_expense/<int:id>/', delete_expense, name="delete-expense"),
]
