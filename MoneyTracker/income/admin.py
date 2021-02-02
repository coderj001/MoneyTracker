from django.contrib import admin
from income.models import Income, Source


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    pass


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    pass
