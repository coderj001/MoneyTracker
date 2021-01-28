from django.urls import path
from core.views import home, add_expense

app_name = 'core'

urlpatterns = [
    path('', home, name="home"),
    path('add_expense', add_expense, name="add-expense"),
]
