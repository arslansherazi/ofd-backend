from configurations.settings.common import *

DEBUG = False

ALLOWED_HOSTS = ['ofd-load-balancer-838337192.us-east-2.elb.amazonaws.com', '18.224.5.209']

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
API_BASE_URL = 'http://18.224.5.209/ofd_apis{}'
BASE_URL = 'http://18.224.5.209'
WSGI_APPLICATION = 'configurations.wsgi.application'
AUTH_USER_MODEL = 'apis.User'
