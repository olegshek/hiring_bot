import ast
import os


def get_env_list(name, default_value=None):
    if name in os.environ:
        return os.environ[name].split(",")

    if default_value is not None:
        return default_value

    raise ValueError('%s not found in environment variables and default_value is None' % name)


def get_env_number(name, default_value=None):
    if name in os.environ:
        try:
            literal_value = ast.literal_eval(os.environ[name])
            if not isinstance(literal_value, float) and not isinstance(literal_value, int):
                raise ValueError
            return literal_value
        except ValueError as e:
            raise ValueError('Invalid value is given for %s' % name) from e

    if default_value is not None:
        return default_value

    raise ValueError('%s not found in environment variables and default_value is None' % name)


def get_env_bool(name, default_value=None):
    if name in os.environ:
        try:
            literal_value = ast.literal_eval(os.environ[name])
            if not isinstance(literal_value, bool):
                raise ValueError
            return literal_value
        except ValueError as e:
            raise ValueError('Invalid value is given for %s' % name) from e

    if default_value is not None:
        return default_value

    raise ValueError('%s not found in environment variables and default_value is None' % name)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_env_bool('DEBUG', False)

ALLOWED_HOSTS = get_env_list('ALLOWED_HOSTS')

# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'core',
    'apps.bot',
    'apps.hiring.apps.HiringConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['POSTGRES_NAME'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': os.environ['POSTGRES_HOST'],
        'PORT': os.environ['POSTGRES_PORT'],
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_L10N = True

USE_TZ = True

gettext = lambda s: s
LANGUAGES = (
    ('ru', gettext('Russian')),
    ('en', gettext('English'))
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

I18N_DOMAIN = os.environ['I18N_DOMAIN']

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']

PRODUCTION_HOST = os.environ['PRODUCTION_HOST']

PG_URL = f"postgres://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:" \
         f"{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_NAME']}"

REDIS_PASSWORD = os.environ['REDIS_DEFAULT_PASSWORD']
REDIS_HOST = os.environ['REDIS_DEFAULT_HOST']
REDIS_PORT = os.environ['REDIS_DEFAULT_PORT']
REDIS_DB = os.environ['REDIS_DEFAULT_DB']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

CANDIDATE_REQUESTS_CHANNEL_ID = os.environ['CANDIDATE_REQUESTS_CHANNEL_ID']
RESUMES_CHANNEL_ID = os.environ['RESUMES_CHANNEL_ID']
