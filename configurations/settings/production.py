from configurations.settings.common import *

DEBUG = False

ALLOWED_HOSTS = ['ofd.pythonanywhere.com']

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
# python any where does not require wsgi configurations. It defines its own wsgi configurations file
WSGI_APPLICATION = 'configurations.wsgi.application'
