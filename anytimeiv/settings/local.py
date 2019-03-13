from .base import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
]

# variable for generate url in html template
SITE_URL = '127.0.0.1:8000'

TIME_ZONE = 'Europe/Kiev'

AUTH_PASSWORD_VALIDATORS = []


ALLOWED_HOSTS += ['*']

INTERNAL_IPS = ['172.29.0.1']


MIDDLEWARE += [
    # ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ...
]

DEBUG_TOOLBAR_PANELS = [
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
]


CONFIG_DEFAULTS = {
    # Toolbar options
    'RESULTS_CACHE_SIZE': 3,
    'SHOW_COLLAPSED': True,
    # Panel options
    'SQL_WARNING_THRESHOLD': 100,   # milliseconds
}

DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }
