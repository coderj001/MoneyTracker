""" production """
import dj_database_url
import os

from .base import *

DEBUG = False


ALLOWED_HOSTS = ["moneytr-app.herokuapp.com"]


DEFAULT_AUTO_FIELD='django.db.models.AutoField'

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}

# logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} '
            '{module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    }
}
