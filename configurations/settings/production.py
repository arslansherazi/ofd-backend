from configurations.settings.common import *

DEBUG = False

ALLOWED_HOSTS = ['onlinefooddepot.pythonanywhere.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'onlinefooddepot.mysql.pythonanywhere-services.com',
        'NAME': 'onlinefooddepot$ofd_db_prod',
        'USER': 'onlinefooddepot',
        'PASSWORD': 'ed9389d6-3157-4755-984f'
    }
}
API_BASE_URL = 'https://onlinefooddepot.pythonanywhere.com/ofd_apis{}'
BASE_URL = 'https://onlinefooddepot.pythonanywhere.com'
# python any where does not require wsgi configurations. It defines its own wsgi configurations file
WSGI_APPLICATION = 'configurations.wsgi.application'
