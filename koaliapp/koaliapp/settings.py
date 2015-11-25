"""
Django settings for koaliapp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2qkyey!2-4vt*ix78)*$ib302c2s!s#614$(%&^z%j22m$)2ic'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'up',
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'koaliapp.urls'

WSGI_APPLICATION = 'koaliapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
	'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'koaliapp',
	'USER':'koali',
	'PASSWORD':'kezai1993',
	'HOST':'localhost', # Set to empty string for localhost.
        'PORT':'', # Set to empty string for default.
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL ='/static/'
STATIC_ROOT = "/usr/webapp/django_kitchen/static/"

MEDIA_ROOT = '/usr/apps/koali_django/media/'
MEDIA_URL = '/site_media/'

FILE_CHARSET = 'utf-8'
DEFAULT_CHARSET = 'utf-8'

TEMPLATE_DIRS = (
        "/usr/apps/koali_django/koaliapps/up/templates",
)

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
CACHES = {
	'default':{
		'BACKEND':'django.core.cache.backends.memcached.MemcachedCache',
		'LOCATION':'120.25.12.205:11211',
		'TIMEOUT':500,
		'OPTIONS':{
			'binary':1,
			'tcp_nodelay':True,
			'ketama':True
			},
		}
}

SESSION_COOKIE_AGE=60*30
SESSION_EXPIRE_AT_BROWSER_CLOSE=True                          
