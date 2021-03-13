from os import environ


from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('expenses.urls')),
    path('auth/', include('authentication.urls')),
    path('preference/', include('userpreferences.urls')),
    path('income/', include('income.urls')),
]

if environ.get('debug') == 'True':
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), ]
