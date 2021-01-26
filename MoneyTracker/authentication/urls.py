from authentication.views import (
    RegistrationView, LoginView, username_validation, email_validation)
from django.urls import path

app_name = 'auth'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('username_validation',
         username_validation, name="username-validation"),
    path('email_validation',
         email_validation, name="email-validation"),
]
