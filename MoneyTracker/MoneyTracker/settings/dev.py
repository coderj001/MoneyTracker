""" development """
import pygments.formatters
from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
]

# For docker config
if environ.get('db') == 'postgresql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'HOST': 'db',
            'POST': 5432,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# django extension
# Always use IPython for shell_plus
SHELL_PLUS = "ipython"

# Truncate sql queries to this number of characters (this is the default)
SHELL_PLUS_PRINT_SQL_TRUNCATE = 1000

# To disable truncation of sql queries use
SHELL_PLUS_PRINT_SQL_TRUNCATE = None

# Specify sqlparse configuration options
# when printing sql queries to the console
SHELL_PLUS_SQLPARSE_FORMAT_KWARGS = dict(
    reindent_aligned=True,
    truncate_strings=500,
)

# Specify Pygments formatter and configuration options when printing
# sql queries to the console
SHELL_PLUS_PYGMENTS_FORMATTER = pygments.formatters.TerminalFormatter
SHELL_PLUS_PYGMENTS_FORMATTER_KWARGS = {}

# debug_toolbar
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.history.HistoryPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]
