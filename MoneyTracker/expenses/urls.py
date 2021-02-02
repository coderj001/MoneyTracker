from expenses.views import (add_expense, delete_expense, edit_expense, home,
                            search_expenses)
from django.urls import path

app_name = 'expenses'

urlpatterns = [
    path('', home, name="home"),
    path('add_expense', add_expense, name="add-expense"),
    path('search_expenses', search_expenses, name="search-expenses"),
    path('edit_expense/<int:id>/', edit_expense, name="edit-expense"),
    path('delete_expense/<int:id>/', delete_expense, name="delete-expense"),
]
