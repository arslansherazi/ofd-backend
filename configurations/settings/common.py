import os
from datetime import timedelta

PROJECT_PATH = os.path.dirname(os.path.realpath(__name__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '9brz#nk)yo0bkl))gerygm@fn!a22+65#@r^39q1&%l!uc+qg*'
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.user',
    'apps.merchant',
    'apps.buyer',
    'corsheaders',
    'rest_framework'
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'security.middlewares.basic_authentication.BasicAuthenticationMiddleware',
    'security.middlewares.security.SecurityMiddleware'
]
# following code is used to disable default authentication middleware
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'security.token_authentication.JWTTokenAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': []
}
ROOT_URLCONF = 'configurations.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_PATH, 'templates')],
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
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=85440)  # 10 years
}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Karachi'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'

# email configurations
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'email-smtp.us-east-2.amazonaws.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'AKIATFPQJWU3755XYXHT'
EMAIL_HOST_PASSWORD = 'BMb/GuVteJ/qopEaP0ZufvrXW0oO0zFwbPf7nviznrFB'

AUTH_USER_MODEL = 'user.User'
