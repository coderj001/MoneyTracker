from django.urls import path
from userpreferences.views import GeneralPrefView

app_name = 'preference'

urlpatterns = [
    path('general/', GeneralPrefView.as_view(), name="general"),
]
