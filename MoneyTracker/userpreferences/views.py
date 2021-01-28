import json

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.views import View
from userpreferences.models import Userpreference


class GeneralPrefView(View):
    def currency_data(self):
        currency_data = list()
        full_path = settings.BASE_DIR.parent / 'currencies.json'
        with open(full_path, "r") as f:
            data = json.load(f)
            for k, v in data.items():
                currency_data.append({'name': k, 'value': v})
        return currency_data

    def currency_pref(self, user):
        user_preferences = Userpreference.objects.get_or_create(
            user=user
        )
        return user_preferences[0].currency

    def get(self, request):
        return render(
            request,
            'preference/index.html',
            context={
                'currencies': self.currency_data(),
                'current_currency': self.currency_pref(request.user)
            }
        )

    def post(self, request):
        currency = request.POST.get('currency')
        user_preferences = Userpreference.objects.get_or_create(
            user=request.user)
        user_preferences[0].currency = currency
        user_preferences[0].save()
        messages.add_message(
            request,
            messages.SUCCESS,
            f"{request.user.username}, preference is saved."
        )
        return render(
            request,
            'preference/index.html',
            context={
                'currencies': self.currency_data(),
                'current_currency': currency
            }
        )
