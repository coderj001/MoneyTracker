from django.contrib import admin
from core.models import Expense, Catagory


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    pass


@admin.register(Catagory)
class CatagoryAdmin(admin.ModelAdmin):
    pass
