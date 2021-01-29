from core.views import add_expense, delete_expense, edit_expense, home
from django.urls import path

app_name = 'core'

urlpatterns = [
    path('', home, name="home"),
    path('add_expense', add_expense, name="add-expense"),
    path('edit_expense/<int:id>/', edit_expense, name="edit-expense"),
    path('delete_expense/<int:id>/', delete_expense, name="delete-expense"),
]
