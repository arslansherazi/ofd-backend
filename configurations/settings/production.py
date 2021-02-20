from configurations.settings.common import *

DEBUG = False

ALLOWED_HOSTS = ['ec2-3-135-230-125.us-east-2.compute.amazonaws.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'ofd.mysql.pythonanywhere-services.com',
        'NAME': 'ofd$ofd_db_prod',
        'USER': 'ofd',
        'PASSWORD': 'ed9389d6-3157-4755-984f',
        'PORT': 3306
    }
}
API_BASE_URL = 'https://onlinefooddepot.pythonanywhere.com/ofd_apis{}'
BASE_URL = 'https://onlinefooddepot.pythonanywhere.com'
WSGI_APPLICATION = 'configurations.wsgi.application'
