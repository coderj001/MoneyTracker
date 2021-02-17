from authentication.views import (LoginView, RegistrationView,
                                  email_validation, logout_user,
                                  username_validation, RequestPasswordResetView)
from django.urls import path

app_name = 'auth'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('request-reset', RequestPasswordResetView.as_view(),
         name="RequestReset"),
    path('username_validation',
         username_validation, name="username-validation"),
    path('email_validation',
         email_validation, name="email-validation"),
    path('logout_user/', logout_user, name="logout-user"),

]
