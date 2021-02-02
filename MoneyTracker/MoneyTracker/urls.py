from os import environ

import debug_toolbar

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('expenses.urls')),
    path('auth/', include('authentication.urls')),
    path('preference/', include('userpreferences.urls')),
]

if environ.get('debug') == 'True':
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), ]
