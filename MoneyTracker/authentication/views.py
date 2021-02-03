import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html', context={})

    def post(self, request):
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        context = {'fieldVal': request.POST}

        if len(password) < 6:
            messages.add_message(request, messages.ERROR,
                                 "Password is too short.")
            return render(request,
                          'authentication/register.html', context=context)

        try:
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Account created successfully.")

            return redirect('auth:login')
        except Exception as e:
            messages.add_message(request, messages.ERROR,
                                 "Please enter unique username and email.")
            return render(request, 'authentication/register.html',
                          context=context)


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html', context={})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if username is None or password is None:
            messages.add_message(request, messages.WARNING,
                                 "Please fill username and password.")
        if user is not None:
            login(request, user)
            messages.add_message(
                request,
                messages.SUCCESS,
                f"Login is successfully. Welcome, {user.username}."
            )
            return redirect("expenses:home-expense")
        else:
            messages.add_message(request, messages.ERROR,
                                 "Please fill correct username and password.")
            return render(request, 'authentication/login.html', context={
                'fieldVal': request.POST,
            })


@login_required
def logout_user(request):
    logout(request)
    return redirect('auth:login')

# Below function is for form validation


@require_POST
@csrf_exempt
def username_validation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')

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


@require_POST
@csrf_exempt
def email_validation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'email_exists':
                'Email already exists.'
            }, status=409)
        else:
            return JsonResponse({
                'email_valid': True
            })
