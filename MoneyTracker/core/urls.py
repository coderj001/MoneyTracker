from django.urls import path
from core.views import home

APP_NAME = 'core'

urlpatterns = [
    path('', home, name="home"),
]
