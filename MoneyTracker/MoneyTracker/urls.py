import debug_toolbar

from os import environ
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('auth/', include('authentication.urls')),
]

if environ.get('debug') == 'True':
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), ]
