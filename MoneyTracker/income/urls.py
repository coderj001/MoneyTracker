from income.views import (home_income, add_income,
                          edit_income, delete_income, search_income)
from django.urls import path

app_name = 'income'

urlpatterns = [
    path('', home_income, name="home-income"),
    path('add_income/', add_income, name="add-income"),
    path('search_income/', search_income, name="search-income"),
    path('edit_income/<int:id>/', edit_income, name="edit-income"),
    path('delete_income/<int:id>/', delete_income, name="delete-income"),
]
