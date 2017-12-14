"""
Django settings for modeling project.

Generated by 'django-admin startproject' using Django 1.11.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from distutils.util import strtobool  # pylint: disable=import-error,no-name-in-module


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#j2)4zppv#a@)6$rvgb#wn#k@a6fc_fa@2dsr9*^vznj!0qmzd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'channels',
    'rest_framework',
    'guardian',
    'mathfilters',
    'versionfield',

    'resolwe',
    'resolwe.permissions',
    'resolwe.flow',
    'resolwe.elastic',
    'resolwe.toolkit',
    'resolwe.test_helpers',

    'resolwe_bio',
    'resolwe_bio.kb',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'modeling.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'modeling.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

ANONYMOUS_USER_ID = -1

# Check if PostgreSQL settings are set via environment variables
pgname = os.environ.get('RESOLWE_POSTGRESQL_NAME', 'resolwe-bio')
pguser = os.environ.get('RESOLWE_POSTGRESQL_USER', 'resolwe')
pghost = os.environ.get('RESOLWE_POSTGRESQL_HOST', 'localhost')
pgport = int(os.environ.get('RESOLWE_POSTGRESQL_PORT', 55433))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': pgname,
        'USER': pguser,
        'HOST': pghost,
        'PORT': pgport,
    }
}


REDIS_CONNECTION = {
    'host': 'localhost',
    'port': int(os.environ.get('RESOLWE_REDIS_PORT', 56380)),
    'db': int(os.environ.get('RESOLWE_REDIS_DATABASE', 0)),
}

FLOW_EXECUTOR = {
    'NAME': 'resolwe.flow.executors.docker',
    # XXX: Change to a stable resolwe image when it will include all the required tools
    'CONTAINER_IMAGE': 'resolwe/bio-linux8-resolwe-preview',
    'CONTAINER_NAME_PREFIX': 'resolwebio',
    'REDIS_CONNECTION': REDIS_CONNECTION,
    'DATA_DIR': os.path.join(BASE_DIR, 'data'),
    'UPLOAD_DIR': os.path.join(BASE_DIR, 'upload'),
    'RUNTIME_DIR': os.path.join(BASE_DIR, 'runtime'),
}
# Set custom executor command if set via environment variable
if 'RESOLWE_DOCKER_COMMAND' in os.environ:
    FLOW_DOCKER_COMMAND = os.environ['RESOLWE_DOCKER_COMMAND']
FLOW_API = {
    'PERMISSIONS': 'resolwe.permissions.permissions',
}
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
    'NAME': 'resolwe.flow.managers.local',
    'REDIS_PREFIX': 'resolwe-bio.manager',
    'REDIS_CONNECTION': REDIS_CONNECTION,
}

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

# Don't pull Docker images if set via the environment variable.
FLOW_DOCKER_DONT_PULL = strtobool(os.environ.get('RESOLWE_DOCKER_DONT_PULL', '0'))

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'resolwe.permissions.filters.ResolwePermissionsFilter',
        'rest_framework_filters.backends.DjangoFilterBackend',
    ),
}

FLOW_PROCESSES_FINDERS = (
    'resolwe.flow.finders.FileSystemProcessesFinder',
    'resolwe.flow.finders.AppDirectoriesFinder',
)

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


# Do not skip tests that fail on Docker executor if this is set via environment
# variable
if os.environ.get('RESOLWEBIO_TESTS_SKIP_DOCKER_FAILURES', '').lower() in ["no", "false"]:
    TESTS_SKIP_DOCKER_FAILURES = False

# Elastic Search.

ELASTICSEARCH_HOST = os.environ.get('RESOLWE_ES_HOST', 'localhost')
ELASTICSEARCH_PORT = int(os.environ.get('RESOLWE_ES_PORT', '59201'))

# Testing.

TEST_RUNNER = 'resolwe.test_helpers.test_runner.ResolweRunner'
TEST_PROCESS_REQUIRE_TAGS = True
# Don't profile unless set via the environment variable.
TEST_PROCESS_PROFILE = strtobool(os.environ.get('RESOLWE_TEST_PROCESS_PROFILE', '0'))

# Channels.

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'asgi_redis.RedisChannelLayer',
        'ROUTING': 'modeling.routing.channel_routing',
        'CONFIG': {
            'hosts': [(REDIS_CONNECTION['host'], REDIS_CONNECTION['port'])],
            'expiry': 3600,
        },
    },
}