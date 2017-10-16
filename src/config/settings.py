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

# Database role that public repos grant access to
# All datahub users are granted access to this role
PUBLIC_ROLE = 'dh_public'
PUBLIC_ROLE_EMAIL = 'noreply+public@datahub.csail.mit.edu'

ANONYMOUS_ROLE = 'dh_anonymous'
ANONYMOUS_ROLE_EMAIL = 'noreply+anon@datahub.csail.mit.edu'

# Where the row level security policies are stored
POLICY_DB = PUBLIC_ROLE
POLICY_SCHEMA = PUBLIC_ROLE
POLICY_TABLE = 'policy'

# Where the licenses are stored
LICENSE_DB = PUBLIC_ROLE
LICENSE_SCHEMA = PUBLIC_ROLE
LICENSE_TABLE = 'license'

# RowLevelSecurity string to mean all users
RLS_ALL = 'ALL'
RLS_PUBLIC = 'PUBLIC'

# Other blacklisted usernames
BLACKLISTED_USERNAMES = [RLS_ALL, RLS_PUBLIC]

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

# /datahub/src/config/settings.py -> /datahub/src/config/ -> /datahub/src/
PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            os.path.join(PROJECT_ROOT, 'templates'),
        ],
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
            ),
        }
    }
]

MIDDLEWARE_CLASSES = (
    # Uncomment the next line and set SECURE_SSL_REDIRECT = True in your
    # local_settings.py to redirect all non-HTTPS requests to HTTPS.
    # 'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'browser.middleware.XForwardedPort',
    'browser.middleware.DataHubManagerExceptionHandler',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'browser.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'browser.wsgi.application'

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
    'rest_framework_swagger',
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
        'read': "Read your DataHub data.",
        'write': "Modify and delete your DataHub data.",
        'profile': "Read your DataHub profile.",
    },
    'READ_SCOPE': 'read',
    'WRITE_SCOPE': 'write',
    'ALLOWED_REDIRECT_URI_SCHEMES': ['http', 'https', 'oauthexplorer'],
    # Access tokens are good for 1 day.
    'ACCESS_TOKEN_EXPIRE_SECONDS': 24 * 60 * 60,
    # Authorization codes must be redeemed within 10 minutes.
    'AUTHORIZATION_CODE_EXPIRE_SECONDS': 600,
    # Refresh tokens never expire. Users can still manually revoke tokens.
    'REFRESH_TOKEN_EXPIRE_SECONDS': None,
    'REQUEST_APPROVAL_PROMPT': 'force',
    'OAUTH2_BACKEND_CLASS':
        'api.oauth2_backends.ContentNegotiatingOAuthLibCore',
}

# DataHub comes with pre-registered OAuth2 Applications.
# You can change these ids for your local instance by overriding in your local
# settings.py. NOTE that changing DATAHUB_DOMAIN in local settings will not
# result in updated redirect_uris here.
OAUTH2_APP_CLIENTS = {
    'console':
        {'name': 'console',
         'client_id': '7ByJAnXj2jsMFN1REvvUarQjqXjIAU3nmVB661hR',
         'redirect_uris': ('https://' + DATAHUB_DOMAIN + '/apps/console/\n'
                           'http://' + DATAHUB_DOMAIN + '/apps/console/\n'
                           'https://web/apps/console/\n'
                           'http://web/apps/console/'),
         'client_type': 'public',
         'authorization_grant_type': 'implicit',
         'skip_authorization': True},
}

OAUTH2_APP_OWNER = '_dh_oauth_user'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'api.permissions.WeakTokenHasReadWriteScope',
    ),
    'EXCEPTION_HANDLER': 'api.views.custom_exception_handler'
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
