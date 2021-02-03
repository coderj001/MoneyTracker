from django.contrib import admin
from expenses.models import Expense, Catagory


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount', 'date', 'category', 'owner', 'description')
    search_fields = ('category', 'owner__username', 'date', 'description')
    list_per_page = 15


@admin.register(Catagory)
class CatagoryAdmin(admin.ModelAdmin):
    pass
