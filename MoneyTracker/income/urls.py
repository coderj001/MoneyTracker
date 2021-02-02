from income.views import (home_income,)
from django.urls import path

app_name = 'income'

urlpatterns = [
    path('', home_income, name="home-income"),
]
