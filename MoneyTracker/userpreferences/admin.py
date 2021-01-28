from django.contrib import admin
from userpreferences.models import Userpreference


@admin.register(Userpreference)
class UserpreferenceAdmin(admin.ModelAdmin):
    pass
