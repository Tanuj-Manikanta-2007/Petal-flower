"""
Django settings for adaptlearn project
RENDER DEPLOYMENT ONLY
"""

from pathlib import Path
import os
import dj_database_url

# ---------------------------------------
# BASE DIR
# ---------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
PETAL_CART_DIR = BASE_DIR

# ---------------------------------------
# SECURITY
# ---------------------------------------
SECRET_KEY = os.environ.get("SECRET_KEY","TANUJ_KEY")

DEBUG = True

ALLOWED_HOSTS = [
    "*",
]

# ---------------------------------------
# APPS
# ---------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'petalcart.apps.BaseConfig',
    'accounts',
    'shop',
]

# ---------------------------------------
# MIDDLEWARE
# ---------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'adaptlearn.urls'

# ---------------------------------------
# TEMPLATES
# ---------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PETAL_CART_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'adaptlearn.context_processors.shopowner_status',
            ],
        },
    },
]

WSGI_APPLICATION = 'adaptlearn.wsgi.application'

# ---------------------------------------
# DATABASE (LOCAL HOST  POSTGRESQL)
# ---------------------------------------

# DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': os.environ.get('DB_NAME', 'petalcart'),
#             'USER': os.environ.get('DB_USER', 'postgres'),
#             'PASSWORD': os.environ.get('DB_PASSWORD', '1590'),
#             'HOST': os.environ.get('DB_HOST', 'localhost'),
#             'PORT': os.environ.get('DB_PORT', '5432'),
#         }
#     }


# ---------------------------------------
# DATABASE (RENDER POSTGRESQL)
# ---------------------------------------

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
    )
}

# ---------------------------------------
# PASSWORD VALIDATION
# ---------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------------------
# INTERNATIONAL
# ---------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------------------------
# STATIC FILES (RENDER + WHITENOISE)
# ---------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ---------------------------------------
# MEDIA FILES (TEMP STORAGE)
# ---------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ---------------------------------------
# DEFAULT FIELD
# ---------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------
# AUTH
# ---------------------------------------
LOGIN_URL = '/accounts/login/'

# ---------------------------------------
# RAZORPAY ENV
# ---------------------------------------
RAZORPAY_KEY_ID = (os.environ.get("RAZORPAY_KEY_ID") or "").strip()
RAZORPAY_KEY_SECRET = (os.environ.get("RAZORPAY_KEY_SECRET") or "").strip()
