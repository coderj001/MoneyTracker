from authentication.views import RegistrationView, LoginView
from django.urls import path

app_name = 'auth'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
]
