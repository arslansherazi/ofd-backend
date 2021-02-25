from configurations.settings.common import *

DEBUG = False

ALLOWED_HOSTS = ['3.22.125.117', '0.0.0.0']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'ofd-db.c4hisjfub95a.us-east-2.rds.amazonaws.com',
        'NAME': 'ofd_db',
        'USER': 'ofd_admin',
        'PASSWORD': 'CHBfXN3L8avPUmBA',
        'PORT': 3306
    }
}
API_BASE_URL = 'http://3.22.125.117/ofd_apis{}'
BASE_URL = 'http://3.22.125.117'
WSGI_APPLICATION = 'configurations.wsgi.application'
AUTH_USER_MODEL = 'apis.User'

# email configurations
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'email-smtp.us-east-2.amazonaws.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 25
EMAIL_HOST_USER = 'AKIATFPQJWU3WMG2QIWL'
EMAIL_HOST_PASSWORD = 'BMCxZXrV31RcsQ/KE6Y0Y9Pk62XsColDeDs0mmvCvmRq'

