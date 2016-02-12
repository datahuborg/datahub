from __future__ import print_function
import sys
import os

from django.db.utils import OperationalError
# DataHub Settings.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Anant Bhardwaj', 'anantb@csail.mit.edu'),
)

MANAGERS = ADMINS

if 'TRAVIS' in os.environ:
    DB_HOST = 'localhost'
    DB_PASSWORD = ''
else:
    DB_HOST = 'db'
    DB_PASSWORD = 'postgres'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'datahub',
        'USER': 'postgres',
        # Change to localhost if not using the Vagrant/Docker setup.
        'PASSWORD': DB_PASSWORD,
        # Docker adds the db container to
        # /etc/hosts automatically.
        # Set to empty string for default. Not used with sqlite3.
        'HOST': DB_HOST,
        'PORT': '5432',
    }
}


TIME_ZONE = 'America/New_York'

# Language code for this installation.
LANGUAGE_CODE = 'en-us'

DATAHUB_DOMAIN = 'datahub-local.mit.edu'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# SECRET_KEY should be unique to each site. Sites should be discouraged
# from using this default key.
try:
    from secret_key import *
except ImportError as e:
    SECRET_KEY = 'k+)#kqr2pgvqm_6y8hq+tj#p12&amp;p%dz#_exvw2x4@##dyz!or*'
    print("Warning: Could not find src/config/secret_key.py. "
          "Using the default SECRET_KEY for now. Run "
          "`src/scripts/generate_secret_key.py` to create a new key.",
          file=sys.stderr)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            )
        }
    }
]

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # Uncomment the next line and set SECURE_SSL_REDIRECT = True in your
    # local_settings.py to redirect all non-HTTPS requests to HTTPS.
    # 'django.middleware.security.SecurityMiddleware',

    'browser.middleware.XForwardedPort',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'browser.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'browser.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'social.apps.django_app.default',
    'rest_framework',
    'oauth2_provider',
    'account',
    'api',
    'console',
    'browser',
    'core',
    'dataq',
    'sentiment',
    'datatables',
    'dbwipes',
    'inventory',
    'refiner',
    'viz2',
    'www'
)

# django.contrib.auth settings
LOGIN_URL = '/account/login'
LOGIN_REDIRECT_URL = '/'
DISCONNECT_REDIRECT_URL = '/account/settings'

# crispy_forms settings
CRISPY_TEMPLATE_PACK = 'bootstrap3'

SOCIAL_AUTH_URL_NAMESPACE = 'social'

# Make sure OAuth redirects use HTTPS, e.g. https://localhost/complete/twitter
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

# Only redirect logins to URLs on this domain.
SOCIAL_AUTH_SANITIZE_REDIRECTS = True

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'account.pipeline.get_user_details',

    # Uncomment to associate new log ins with existing accounts using the same
    # email address. A security vulnerability if identity providers who don't
    # verify email addresses are allowed.
    # 'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',

    # Uncomment to keeps things like the user's real name and email address up
    # to date. DataHub doesn't need to know someone's real name.
    # 'social.pipeline.user.user_details',
)

SOCIAL_AUTH_DISCONNECT_PIPELINE = (
    'account.pipeline.set_password_if_needed',
    'social.pipeline.disconnect.allowed_to_disconnect',
    'social.pipeline.disconnect.get_entries',
    'social.pipeline.disconnect.revoke_tokens',
    'social.pipeline.disconnect.disconnect'
)

SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['preferred_username']

SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['username', 'email']

OAUTH2_PROVIDER = {
    'SCOPES': {
        'read': "Read something",
        'write': "Sure, why not",
    },
    'ALLOWED_REDIRECT_URI_SCHEMES': ['http', 'https', 'oauthexplorer'],
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Instances should create a local_settings.py to define custom settings.
try:
    from local_settings import *
    # Only set the Site model if local_settings exists. Otherwise assume this
    # is a Travis CI build and that the domain doesn't matter.
    from site_utils import set_site_info
    set_site_info(domain=DATAHUB_DOMAIN)
except ImportError:
    from default_settings import *
except OperationalError:
    # DB access fails during docker build. Ignore that here so the
    # collectstatic call will succeed.
    pass
