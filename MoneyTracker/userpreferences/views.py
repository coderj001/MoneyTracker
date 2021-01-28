import json

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.views import View
from userpreferences.models import Userpreference


class GeneralPrefView(View):
    def get(self, request):
        currency_data = list()

        full_path = settings.BASE_DIR.parent / 'currencies.json'
        with open(full_path, "r") as f:
            data = json.load(f)
            for k, v in data.items():
                currency_data.append({'name': k, 'value': v})

        return render(
            request,
            'preference/index.html',
            context={'currencies': currency_data}
        )

    def post(self, request):
        currency = request.POST.get('currency')
        user_preferences = Userpreference.objects.get(user=request.user)
        user_preferences.currency = currency
        user_preferences.save()
        messages.add_messages(
            request,
            messages.SUCCESS,
            f"{request.user.username}, preference is saved."
        )
