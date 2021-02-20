from django.urls import path
from income.views import (add_income, delete_income, edit_income, home_income,
                          income_source_summery, income_summery, search_income)

app_name = 'income'

urlpatterns = [
    path('', home_income, name="home-income"),
    path('add_income', add_income, name="add-income"),
    path('search_income', search_income, name="search-income"),
    path('income_summery', income_summery,
         name="income-summery"),
    path('income_source_summery', income_source_summery,
         name="income-source-summery"),
    path('edit_income/<int:id>/', edit_income, name="edit-income"),
    path('delete_income/<int:id>/', delete_income, name="delete-income"),
]
