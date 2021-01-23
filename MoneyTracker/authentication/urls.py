from authentication.views import RegistrationView
from django.urls import path

APP_NAME = 'auth'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name="register"),
]
