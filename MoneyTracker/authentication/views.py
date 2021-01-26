from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html', context={})


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html', context={})


@csrf_exempt
def username_validation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse(
                {
                    'username_error':
                    'Username should only contain alphanumeric characters.'
                },
                status=400
            )
        elif User.objects.filter(username=username).exists():
            return JsonResponse(
                {
                    'username_exists':
                    'Username already exists.'
                },
                status=409
            )

        return JsonResponse({'username_valid': True})
