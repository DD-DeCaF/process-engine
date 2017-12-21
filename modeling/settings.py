import os
import sys
import re
from distutils.util import strtobool  # pylint: disable=import-error,no-name-in-module



PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

SECRET_KEY = 'set-this-in-production'

ALLOWED_HOSTS = ['*.genialis.com', 'localhost']

# Application definition.

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'raven.contrib.django.raven_compat',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_reactive',
    'rest_auth',
    'guardian',
    'mathfilters',
    'versionfield',
    'corsheaders',
    'simple_history',
    'channels',
    'django_filters',

    'resolwe',
    'resolwe.permissions',
    'resolwe.flow',
    'resolwe.elastic',
    'resolwe.toolkit',

    'resolwe_bio',
    'resolwe_bio.kb',

    'modeling'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
)


TEST_RUNNER = 'resolwe.test_helpers.test_runner.ResolweRunner'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'modeling.wsgi.application'

# Database.

# Check if PostgreSQL settings are set via environment variables
# pylint: disable=invalid-name
pgname = os.environ.get('GENESIS_POSTGRESQL_NAME', 'resolwe-genialis')
pguser = os.environ.get('GENESIS_POSTGRESQL_USER', 'resolwe')
pghost = os.environ.get('GENESIS_POSTGRESQL_HOST', 'localhost')
pgport = int(os.environ.get('GENESIS_POSTGRESQL_PORT', 5432))

DATABASES = {
    'default': {
        'ENGINE': 'django_db_geventpool.backends.postgresql_psycopg2',
        'NAME': pgname,
        'USER': pguser,
        'HOST': pghost,
        'PORT': pgport,
        'CONN_MAX_AGE': 0,
        'OPTIONS': {
            'MAX_CONNS': 20,
        },
    },
}


# Internationalization.

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/Ljubljana'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images).

STATIC_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, '..', 'static'))

STATIC_URL = '/static/'

GENJS_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, '..', 'frontend'))

STATICFILES_DIRS = (
    GENJS_ROOT,
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# Authentication.

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

ANONYMOUS_USER_NAME = 'public'


HOST = os.environ.get('DOCKER_HOST', 'localhost')


REDIS_CONNECTION = {
    'host': HOST,
    'port': int(os.environ.get('GENESIS_REDIS_PORT', 56381)),
    'db': int(os.environ.get('GENESIS_REDIS_DATABASE', 1)),
}

# Channels

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'asgi_redis.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(REDIS_CONNECTION['host'], REDIS_CONNECTION['port'])],
            'expiry': 3600,
        },
        'ROUTING': 'modeling.routing.channel_routing',
    },
}


# CORS

CORS_ORIGIN_REGEX_WHITELIST = (
    r'^(https?:\/\/)?(\w+\.)?(localhost|127.0.0.1)(:\d+)$',
)

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'session-id',
    'x-file-uid',
)


# Resolwe.

FLOW_EXECUTOR = {
    'NAME': 'resolwe.flow.executors.docker',
    'DATA_DIR': os.path.abspath(os.path.join(PROJECT_ROOT, 'data/data')),
    'UPLOAD_DIR': os.path.abspath(os.path.join(PROJECT_ROOT, 'data/upload')),
    'RUNTIME_DIR': os.path.abspath(os.path.join(PROJECT_ROOT, 'data/runtime')),
    'CONTAINER_IMAGE': 'resolwe/bio-linux8-resolwe-preview',
    'REDIS_CONNECTION': REDIS_CONNECTION,
    'TEST': {
        'DATA_DIR': os.path.abspath(os.path.join(PROJECT_ROOT, 'data/test_data')),
        'UPLOAD_DIR': os.path.abspath(os.path.join(PROJECT_ROOT, 'data/test_upload')),
        'RUNTIME_DIR': os.path.abspath(os.path.join(PROJECT_ROOT, 'data/test_runtime')),
    }
}

# Set custom executor command if set via environment variable
if 'GENESIS_DOCKER_COMMAND' in os.environ:
    FLOW_DOCKER_COMMAND = os.environ['GENESIS_DOCKER_COMMAND']

FLOW_EXPRESSION_ENGINES = [
    {
        'ENGINE': 'resolwe.flow.expression_engines.jinja',
        'CUSTOM_FILTERS': [
            'resolwe_bio.expression_filters.sample',
        ]
    },
]
FLOW_EXECUTION_ENGINES = [
    'resolwe.flow.execution_engines.bash',
    'resolwe.flow.execution_engines.workflow',
]


FLOW_MANAGER = {
    'NAME': 'resolwe.flow.managers.celery',
    'REDIS_PREFIX': 'genialis-base.manager',
    'REDIS_CONNECTION': REDIS_CONNECTION,
    'TEST': {
        'REDIS_PREFIX': 'genialis-base.manager-test'
    },
}

BROKER_URL = 'redis://{host}:{port}/{db}'.format(**REDIS_CONNECTION)

# NOTE: Since FLOW_EXECUTOR['DATA_DIR'] and FLOW_EXECUTOR['UPLOAD_DIR'] are
# shared among all containers they must use the shared SELinux label (z
# option). Each Data object's subdirectory under FLOW_EXECUTOR['DATA_DIR'] can
# use its unique SELinux label (Z option).
FLOW_DOCKER_MAPPINGS = [
    {'src': os.path.join(FLOW_EXECUTOR['DATA_DIR'], '{data_id}'),
     'dest': '/data',
     'mode': 'rw,Z'},
    {'src': FLOW_EXECUTOR['DATA_DIR'],
     'dest': '/data_all',
     'mode': 'ro,z'},
    {'src': FLOW_EXECUTOR['UPLOAD_DIR'],
     'dest': '/upload',
     'mode': 'rw,z'},
]

FLOW_API = {
    'PERMISSIONS': 'resolwe.permissions.permissions',
}

FLOW_PROCESSES_FINDERS = (
    'resolwe.flow.finders.FileSystemProcessesFinder',
    'resolwe.flow.finders.AppDirectoriesFinder',
)

RESOLWE_HOST_URL = 'http://localhost:8000'

# REST framework.

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_filters.backends.DjangoFilterBackend',
        # 'modeling.base.filters.JsonOrderingFilter',
        'resolwe.permissions.filters.ResolwePermissionsFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'EXCEPTION_HANDLER': 'resolwe.flow.utils.exceptions.resolwe_exception_handler',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}


# REST framework reactive.

DJANGO_REST_FRAMEWORK_REACTIVE = {
    'host': 'localhost',
    'port': 9432,
}


# Cache.

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://{host}:{port}/{db}'.format(**REDIS_CONNECTION),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}


# Session.

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

SESSION_CACHE_ALIAS = 'default'


# Search

ELASTICSEARCH_HOST = os.environ.get('GENESIS_ES_HOST', 'localhost')
ELASTICSEARCH_PORT = int(os.environ.get('GENESIS_ES_PORT', 9200))
ELASTICSEARCH_INDEX_PREFIX = 'test_' if 'test' in sys.argv else ''

# Logging.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'sentry'],
            'level': 'INFO',
        },
        'raven': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
        'elasticsearch': {
            'handlers': ['console', 'sentry'],
            'level': 'WARNING',
            'propagate': False,
        },
        'urllib3': {
            'handlers': ['console', 'sentry'],
            'level': 'WARNING',
            'propagate': False,
        },
    }
}


# PhantomJS

PHANTOMJS_PATH = os.environ.get('GENESIS_PHANTOMJS_PATH', '/usr/bin/phantomjs')


# Configuration.

CONFIGURATION_SCHEMA_PATH = os.path.join(GENJS_ROOT, 'genjs', 'schema', 'configuration.json')


# Registration.

USER_ACTIVATION_URL = 'http://localhost:3000/{community}/user/activate'
USER_PASSWORD_RESET_URL = 'http://localhost:3000/{community}/user/reset_password'

# Newsletter.

MAILCHIMP_USERNAME = ''
MAILCHIMP_API_KEY = ''
MAILCHIMP_NEWSLETTER_LIST = 'da77748be9'  # This is the 'QA Testing' list.

# E-mail.

EMAIL_SUBJECT_PREFIX = "[Genialis Platform] "

# Sentry configuration

RAVEN_CONFIG = {
    # 'dsn': '',  # NOTE: set in production
    'release': '0.1',
}

DEBUG = True


MANAGERS = [
    ('The Boss', 'boss@localhost'),
]

# If using Docker on Mac OSX or Windows
if HOST != 'localhost':
    HOST = re.search(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}', HOST)
    HOST = HOST.group() if HOST else 'localhost'


pghost = os.environ.get('GENESIS_POSTGRESQL_HOST', HOST)  # pylint: disable=invalid-name
pgport = int(os.environ.get('GENESIS_POSTGRESQL_PORT', 55434))  # pylint: disable=invalid-name


channels_config = {  # pylint: disable=invalid-name
    'hosts': [(REDIS_CONNECTION['host'], REDIS_CONNECTION['port'])],
    'expiry': 3600,
}

CHANNEL_LAYERS['default']['CONFIG'] = channels_config
CHANNEL_LAYERS['default']['TEST_CONFIG'] = channels_config

FLOW_EXECUTOR['REDIS_CONNECTION'] = REDIS_CONNECTION

FLOW_MANAGER['REDIS_CONNECTION'] = REDIS_CONNECTION

WS4REDIS_CONNECTION = REDIS_CONNECTION

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Set custom ReSDK location if set via environment variable
if 'GENESIS_RESDK_PATH' in os.environ:
    RESDK_PATH = os.environ['GENESIS_RESDK_PATH']

# Testing Django LiveServer's configuration.
TEST_LIVESERVER_HOST = os.environ.get('GENESIS_TEST_LIVESERVER_HOST', 'localhost')
TEST_LIVESERVER_PORT = int(os.environ.get('GENESIS_TEST_LIVESERVER_PORT', 8080))

# Don't pull Docker images if set via the environment variable.
FLOW_DOCKER_DONT_PULL = strtobool(os.environ.get('GENESIS_DOCKER_DONT_PULL', '1'))

ROOT_URLCONF = 'modeling.urls'
